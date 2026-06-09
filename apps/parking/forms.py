from django import forms

from .models import ParkingSpot, Subscription


class ParkingSpotForm(forms.ModelForm):
    class Meta:
        model = ParkingSpot
        exclude = ()


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        exclude = ()
