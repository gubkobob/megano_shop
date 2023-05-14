from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "id", "name", "slug"
    list_display_links = "id", "name", "slug"
    search_fields = "name",
    prepopulated_fields = {"slug": ("name",)}


# class ShopAdmin(admin.ModelAdmin):
#     """
#     Админ панель модели Shop
#     """
#     list_display = ['name', 'descriptions', 'address', 'phone', 'email', 'image', 'product']
#
# admin.site.register(Shop, ShopAdmin)