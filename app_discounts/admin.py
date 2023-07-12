from django.contrib import admin
from .models import (
    Discount,
    Coupon
)
from django import forms


class DiscountAdminForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Админ панель модель Specifications"""
    list_display = [
        'id',
        'product_id',
        'product',
        'type_discount',
        'start_discount',
        'end_discount',
        'available',
    ]
    form = DiscountAdminForm


class CouponAdminForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
    form = CouponAdminForm

