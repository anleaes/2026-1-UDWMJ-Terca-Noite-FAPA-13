from django.db import models

from customers.models import Customer


class ParkingSpot(models.Model):
    STATUS_LIVRE = 'Livre'
    STATUS_OCUPADA = 'Ocupada'
    STATUS_RESERVADA = 'Reservada'

    STATUS_CHOICES = [
        (STATUS_LIVRE, 'Livre'),
        (STATUS_OCUPADA, 'Ocupada'),
        (STATUS_RESERVADA, 'Reservada'),
    ]

    number = models.CharField(max_length=10, verbose_name='Número')
    is_covered = models.BooleanField(default=False, verbose_name='Coberta')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_LIVRE,
        verbose_name='Status',
    )
    occupied_since = models.DateTimeField(null=True, blank=True, verbose_name='Ocupada desde')

    class Meta:
        ordering = ['id']
        verbose_name = 'Vaga'
        verbose_name_plural = 'Vagas'

    def __str__(self):
        return self.number


class Subscription(models.Model):
    start_date = models.DateField(verbose_name='Data de Início')
    end_date = models.DateField(verbose_name='Data de Término')
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Mensalidade')
    is_active = models.BooleanField(default=True, verbose_name='Ativa')
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Cliente',
    )
    parking_spot = models.OneToOneField(
        ParkingSpot,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Vaga',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Assinatura'
        verbose_name_plural = 'Assinaturas'

    def __str__(self):
        return f'{self.customer} - {self.parking_spot}'
