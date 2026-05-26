from django.db import models


class Socialnetwork(models.Model):
    name = models.CharField('Nome', max_length=50)
    content_type = models.TextField('Tipo de conteúdo', max_length=100)
    url = models.CharField('URL da Rede Social', max_length=200)

    class Meta:
        verbose_name = 'Rede Social'
        verbose_name_plural = 'Redes Sociais'
        ordering = ['id']

    def __str__(self):
        return f'{self.name}'


class Person(models.Model):
    first_name = models.CharField('Nome', max_length=50)
    last_name = models.CharField('Sobrenome', max_length=100)
    address = models.CharField('Endereço', max_length=200)
    phone = models.CharField('Telefone celular', max_length=20)
    email = models.EmailField('E-mail', null=False, blank=False)

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ['id']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Client(Person):
    gender = models.CharField('Gênero', max_length=1, choices=[
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ])
    socialnetwork = models.ManyToManyField(Socialnetwork, verbose_name="Redes Sociais", blank=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Employee(Person):
    salary = models.FloatField('Salário', null=True, blank=True, default=0.0)
    position = models.CharField('Cargo', max_length=100)
    hire_date = models.DateField('Data de Contratação', null=True, blank=True)
    is_active = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['id']
