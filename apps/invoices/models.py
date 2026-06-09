from django.db import models

from operations.models import ServiceOrder


class Invoice(models.Model):
    number = models.CharField(max_length=20, unique=True, verbose_name='Número')
    issue_date = models.DateField(verbose_name='Data de Emissão')
    service_order = models.OneToOneField(
        ServiceOrder,
        on_delete=models.CASCADE,
        related_name='invoice',
        verbose_name='Ordem de Serviço',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Nota Fiscal'
        verbose_name_plural = 'Notas Fiscais'

    def __str__(self):
        return self.number
