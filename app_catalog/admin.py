from django.contrib import admin
from .models import *


class ShopAdmin(admin.ModelAdmin):
    """
    Админ панель модели Shop
    """
    list_display = ['name', 'descriptions', 'address', 'phone', 'email', 'image', 'product']

admin.site.register(Shop, ShopAdmin)