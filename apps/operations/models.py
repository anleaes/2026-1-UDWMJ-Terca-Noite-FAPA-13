from django.db import models

from customers.models import Customer, Vehicle
from parking.models import ParkingSpot


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    base_price = models.FloatField(verbose_name='Preço Base')

    class Meta:
        ordering = ['id']
        verbose_name = 'Categoria de Serviço'
        verbose_name_plural = 'Categorias de Serviço'

    def __str__(self):
        return self.name


class ServiceOrder(models.Model):
    STATUS_ABERTA = 'Aberta'
    STATUS_FINALIZADA = 'Finalizada'

    STATUS_CHOICES = [
        (STATUS_ABERTA, 'Aberta'),
        (STATUS_FINALIZADA, 'Finalizada'),
    ]

    entry_time = models.DateTimeField(verbose_name='Entrada')
    exit_time = models.DateTimeField(verbose_name='Saída', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ABERTA, verbose_name='Status')
    total = models.FloatField(default=0, verbose_name='Total')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Cliente')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name='Veículo')
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, verbose_name='Vaga')

    class Meta:
        ordering = ['id']
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'

    def __str__(self):
        return f'Ordem {self.id} - {self.customer}'


class ServiceItem(models.Model):
    quantity = models.PositiveIntegerField(verbose_name='Quantidade')
    unit_price = models.FloatField(verbose_name='Preço Unitário')
    subtotal = models.FloatField(verbose_name='Subtotal')
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, verbose_name='Categoria')
    service_order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE, related_name='items', verbose_name='Ordem')

    class Meta:
        ordering = ['id']
        verbose_name = 'Item de Serviço'
        verbose_name_plural = 'Itens de Serviço'

    def __str__(self):
        return f'{self.service_category} x {self.quantity}'
