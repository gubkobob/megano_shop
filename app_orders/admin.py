from django.contrib import admin
from .models import OrderItem, Order


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = "id", "quantity", "price", "order", "product"
    list_display_links = "id", "quantity", "price", "order", "product"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "id", "first_name"
    list_display_links = "id", "first_name"