from django import forms

from app_users.services import get_10_digits_from_phone_number

from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ("full_name", "phone_number", "email", "city", "address", "buying_type", "payment", "comment", "status")
