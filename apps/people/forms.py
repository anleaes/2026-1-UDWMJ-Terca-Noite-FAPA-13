from django import forms

from .models import Client, Employee, Socialnetwork


class SocialnetworkForm(forms.ModelForm):
    class Meta:
        model = Socialnetwork
        exclude = ()


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ()


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ()
