from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Nome')
    last_name = models.CharField(max_length=100, verbose_name='Sobrenome')
    cpf = models.CharField(max_length=14, verbose_name='CPF')
    phone = models.CharField(max_length=20, verbose_name='Telefone')
    email = models.EmailField(verbose_name='E-mail')

    class Meta:
        abstract = True


class Customer(Person):
    is_monthly = models.BooleanField(default=False, verbose_name='Mensalista')

    class Meta:
        ordering = ['id']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=10, verbose_name='Placa')
    model = models.CharField(max_length=100, verbose_name='Modelo')
    color = models.CharField(max_length=50, verbose_name='Cor')
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='vehicles',
        verbose_name='Cliente',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'

    def __str__(self):
        return self.license_plate
