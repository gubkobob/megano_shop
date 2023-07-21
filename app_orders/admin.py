from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Админ панель модели Товары в заказе
    """

    model = OrderItem
    raw_id_fields = ["product_in_shop"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Админ панель модели Заказов
    """

    inlines = [OrderItemInline]
    list_display = (
        "id",
        "user",
        "full_name",
        "phone_number",
        "email",
        "city",
        "address",
        "delivery",
        "delivery_cost",
        "coupon",
        "discount",
        "payment",
        "comment",
        "created_at",
        "status",
    )
    list_display_links = "id", "user", "full_name"
    search_fields = (
        "id",
        "user",
        "full_name",
        "phone_number",
        "email",
        "city",
        "address",
        "delivery",
        "delivery_cost",
        "coupon",
        "discount",
        "payment",
        "created_at",
        "status",
    )
    list_filter = (
        "id",
        "user",
        "full_name",
        "city",
        "delivery",
        "delivery_cost",
        "coupon",
        "discount",
        "payment",
        "status",
    )
