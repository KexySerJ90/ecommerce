from django import forms
from django.core.validators import EmailValidator

from .models import ShippingAdress

class ShippingForm(forms.ModelForm):
    class Meta:
        model=ShippingAdress
        fields = ['full_name', 'email', 'address1', 'address2', 'city', 'state', 'zipcode']
        exclude=['user',]
        labels = {'full_name': 'Full name*','email':'Email*', 'address1': 'Address1*','address2': 'Address2*', 'city':'City*' }
        widgets = {
            field: forms.TextInput(attrs={"class":"form-control validate", 'placeholder': field.capitalize(), 'autocomplete':'off'}) for field in fields
            if field != 'email'
        }
        widgets['email'] = forms.EmailInput(attrs={"class": "form-control validate", 'placeholder': 'Email', 'autocomplete':'off'})


