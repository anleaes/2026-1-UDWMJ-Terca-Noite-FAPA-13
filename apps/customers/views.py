from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomerForm
from .models import Customer


def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_customers')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Adicionar Cliente'})


def list_customers(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})


def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('list_customers')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Editar Cliente'})


def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('list_customers')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})


def search_customers(request):
    query = request.GET.get('q', '')
    customers = Customer.objects.filter(last_name__icontains=query) if query else Customer.objects.none()
    return render(request, 'customers/customer_search.html', {'customers': customers, 'query': query})
