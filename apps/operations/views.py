import math

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from customers.models import Customer, Vehicle
from parking.models import ParkingSpot

from invoices.views import create_invoice_for_order

from .models import ServiceCategory, ServiceItem, ServiceOrder

PARKING_RATE_PER_MINUTE = 15


def get_cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
    return request.session['cart']


def get_occupancy_data(spot):
    if not spot.occupied_since:
        return None
    delta = timezone.now() - spot.occupied_since
    total_seconds = int(delta.total_seconds())
    total_minutes = max(1, math.ceil(total_seconds / 60))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return {
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'total_minutes': total_minutes,
        'estimated_cost': total_minutes * PARKING_RATE_PER_MINUTE,
        'display': f'{hours}h {minutes}min {seconds}s',
    }


def list_items(request):
    occupied_spots = []
    for spot in ParkingSpot.objects.filter(status=ParkingSpot.STATUS_OCUPADA):
        if not spot.occupied_since:
            spot.occupied_since = timezone.now()
            spot.save(update_fields=['occupied_since'])
        occupancy = get_occupancy_data(spot)
        occupied_spots.append({
            'spot': spot,
            'occupancy': occupancy,
        })
    categories = ServiceCategory.objects.all()
    return render(request, 'operations/list_items.html', {
        'occupied_spots': occupied_spots,
        'categories': categories,
        'parking_rate': PARKING_RATE_PER_MINUTE,
    })


def cart(request):
    cart_items = []
    total = 0
    for item in get_cart(request):
        category = get_object_or_404(ServiceCategory, pk=item['category_id'])
        subtotal = item['quantity'] * category.base_price
        total += subtotal
        cart_items.append({
            'category': category,
            'quantity': item['quantity'],
            'subtotal': subtotal,
        })
    spot_id = request.GET.get('spot_id') or request.session.get('spot_id')
    spot = None
    occupancy = None
    if spot_id:
        spot = get_object_or_404(ParkingSpot, pk=spot_id, status=ParkingSpot.STATUS_OCUPADA)
        if not spot.occupied_since:
            spot.occupied_since = timezone.now()
            spot.save(update_fields=['occupied_since'])
        occupancy = get_occupancy_data(spot)
        request.session['spot_id'] = spot.id
        request.session.modified = True
    return render(request, 'operations/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'spot': spot,
        'occupancy': occupancy,
        'parking_rate': PARKING_RATE_PER_MINUTE,
        'customers': Customer.objects.all(),
        'vehicles': Vehicle.objects.all(),
    })


def add_to_cart(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        quantity = int(request.POST.get('quantity', 1))
        spot_id = request.POST.get('spot_id')
        get_object_or_404(ServiceCategory, pk=category_id)
        cart = get_cart(request)
        found = False
        for item in cart:
            if item['category_id'] == int(category_id):
                item['quantity'] += quantity
                found = True
                break
        if not found:
            cart.append({'category_id': int(category_id), 'quantity': quantity})
        request.session['cart'] = cart
        if spot_id:
            request.session['spot_id'] = int(spot_id)
        request.session.modified = True
        if spot_id:
            return redirect(f'{reverse("cart")}?spot_id={spot_id}')
    return redirect('cart')


def checkout(request):
    if request.method != 'POST':
        return redirect('list_items')

    spot = get_object_or_404(
        ParkingSpot,
        pk=request.POST.get('parking_spot_id'),
        status=ParkingSpot.STATUS_OCUPADA,
    )
    customer = get_object_or_404(Customer, pk=request.POST.get('customer_id'))
    vehicle = get_object_or_404(Vehicle, pk=request.POST.get('vehicle_id'))

    entry_time = spot.occupied_since or timezone.now()
    exit_time = timezone.now()
    duration_seconds = (exit_time - entry_time).total_seconds()
    total_minutes = max(1, math.ceil(duration_seconds / 60))
    parking_subtotal = total_minutes * PARKING_RATE_PER_MINUTE

    order = ServiceOrder.objects.create(
        entry_time=entry_time,
        exit_time=exit_time,
        status=ServiceOrder.STATUS_FINALIZADA,
        total=0,
        customer=customer,
        vehicle=vehicle,
        parking_spot=spot,
    )

    parking_category, _ = ServiceCategory.objects.get_or_create(
        name='Estacionamento',
        defaults={'base_price': PARKING_RATE_PER_MINUTE},
    )

    total = parking_subtotal
    ServiceItem.objects.create(
        quantity=total_minutes,
        unit_price=PARKING_RATE_PER_MINUTE,
        subtotal=parking_subtotal,
        service_category=parking_category,
        service_order=order,
    )

    cart = get_cart(request)
    for item in cart:
        category = get_object_or_404(ServiceCategory, pk=item['category_id'])
        subtotal = item['quantity'] * category.base_price
        ServiceItem.objects.create(
            quantity=item['quantity'],
            unit_price=category.base_price,
            subtotal=subtotal,
            service_category=category,
            service_order=order,
        )
        total += subtotal

    order.total = total
    order.save()

    spot.status = ParkingSpot.STATUS_LIVRE
    spot.occupied_since = None
    spot.save()

    request.session['cart'] = []
    request.session.pop('spot_id', None)
    request.session.modified = True

    invoice = create_invoice_for_order(order)

    return render(request, 'operations/checkout_success.html', {
        'order': order,
        'total_minutes': total_minutes,
        'parking_subtotal': parking_subtotal,
        'invoice': invoice,
    })
