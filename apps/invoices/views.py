from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Invoice


def generate_invoice_number():
    now = timezone.now()
    prefix = f'NF{now.year}{now.month:02d}'
    last_invoice = Invoice.objects.filter(number__startswith=prefix).order_by('-number').first()
    if last_invoice:
        sequence = int(last_invoice.number[len(prefix):]) + 1
    else:
        sequence = 1
    return f'{prefix}{sequence:04d}'


def create_invoice_for_order(order):
    return Invoice.objects.create(
        number=generate_invoice_number(),
        issue_date=timezone.now().date(),
        service_order=order,
    )


def view_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'invoices/invoice.html', {'invoice': invoice})
