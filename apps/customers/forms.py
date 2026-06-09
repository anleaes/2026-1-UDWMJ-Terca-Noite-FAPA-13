from django import forms

from .models import Customer, Vehicle


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ()


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ()
