from django.contrib import admin
from .models import Discount, DiscountPrice
from django import forms


class DiscountAdminForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'


class DiscountPriceInline(admin.TabularInline):
    model = DiscountPrice


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Админ панель модель Specifications"""
    list_display = [
        'product',
        'type_discount',
        'start_discount',
        'end_discount',
    ]
    form = DiscountAdminForm
    inlines = [DiscountPriceInline]
