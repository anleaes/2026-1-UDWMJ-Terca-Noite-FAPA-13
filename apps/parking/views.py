from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ParkingSpotForm, SubscriptionForm
from .models import ParkingSpot, Subscription


def list_parking_spots(request):
    spots = ParkingSpot.objects.all()
    return render(request, 'parking/parking_spot_list.html', {'spots': spots})


def add_parking_spot(request):
    if request.method == 'POST':
        form = ParkingSpotForm(request.POST)
        if form.is_valid():
            spot = form.save(commit=False)
            if spot.status == ParkingSpot.STATUS_OCUPADA:
                spot.occupied_since = timezone.now()
            spot.save()
            return redirect('list_parking_spots')
    else:
        form = ParkingSpotForm()
    return render(request, 'parking/parking_spot_form.html', {'form': form, 'title': 'Adicionar Vaga'})


def edit_parking_spot(request, pk):
    spot = get_object_or_404(ParkingSpot, pk=pk)
    if request.method == 'POST':
        form = ParkingSpotForm(request.POST, instance=spot)
        if form.is_valid():
            updated_spot = form.save(commit=False)
            if updated_spot.status == ParkingSpot.STATUS_OCUPADA:
                if not updated_spot.occupied_since:
                    updated_spot.occupied_since = timezone.now()
            else:
                updated_spot.occupied_since = None
            updated_spot.save()
            return redirect('list_parking_spots')
    else:
        form = ParkingSpotForm(instance=spot)
    return render(request, 'parking/parking_spot_form.html', {'form': form, 'title': 'Editar Vaga'})


def delete_parking_spot(request, pk):
    spot = get_object_or_404(ParkingSpot, pk=pk)
    if request.method == 'POST':
        spot.delete()
        return redirect('list_parking_spots')
    return render(request, 'parking/parking_spot_confirm_delete.html', {'spot': spot})


def list_subscriptions(request):
    subscriptions = Subscription.objects.all()
    return render(request, 'parking/subscription_list.html', {'subscriptions': subscriptions})


def add_subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_subscriptions')
    else:
        form = SubscriptionForm()
    return render(request, 'parking/subscription_form.html', {'form': form, 'title': 'Adicionar Assinatura'})


def edit_subscription(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('list_subscriptions')
    else:
        form = SubscriptionForm(instance=subscription)
    return render(request, 'parking/subscription_form.html', {'form': form, 'title': 'Editar Assinatura'})


def delete_subscription(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    if request.method == 'POST':
        subscription.delete()
        return redirect('list_subscriptions')
    return render(request, 'parking/subscription_confirm_delete.html', {'subscription': subscription})
