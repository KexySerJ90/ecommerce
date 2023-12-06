from django import forms
from .models import ShippingAdress

class ShippingForm(forms.ModelForm):
    class Meta:
        model=ShippingAdress
        fields = ['full_name', 'email', 'address1', 'address2', 'city', 'state', 'zipcode']
        exclude=['user',]