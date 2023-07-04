from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Админ панель модели Заказов
    """
    list_display = "id", "full_name", "phone_number", "email", "city", "address", \
                   "buying_type", "payment", "comment", "created_at", "status"
    list_display_links = "id", "full_name"
    search_fields = "id", "full_name", "phone_number", "email", "city", "address", "buying_type", \
                    "payment", "created_at", "status"
    list_filter = "id", "full_name", "city", "buying_type", "payment", "status"

