from django.contrib import admin
from .models import Discount
from django import forms


class DiscountAdminForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Админ панель модель Specifications"""
    list_display = [
        'product',
        # 'auto_price',
        'discount',
        'start_discount',
        'end_discount',
    ]
    form = DiscountAdminForm

    #
    # def auto_price(self, obj: Discount):
    #     return obj.product.price
