from django import forms
from django.contrib import admin

from .models import Coupon, Discount


class DiscountAdminForm(forms.ModelForm):
    """Форма для модели Discount"""
    class Meta:
        model = Discount
        fields = "__all__"


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Админ панель модель Discount"""

    list_display = [
        "id",
        "product_id",
        "product",
        "type_discount",
        "start_discount",
        "end_discount",
        "available",
    ]
    form = DiscountAdminForm


class CouponAdminForm(forms.ModelForm):
    """Форма для модели Coupon"""
    class Meta:
        model = Coupon
        fields = "__all__"


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """Админ панель модель Coupon"""
    list_display = ["code", "valid_from", "valid_to", "discount", "active"]
    list_filter = ["active", "valid_from", "valid_to"]
    search_fields = ["code"]
    form = CouponAdminForm
