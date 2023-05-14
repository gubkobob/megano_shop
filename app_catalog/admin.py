from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админ панель модели Категории товаров
    """
    list_display = "id", "name", "slug"
    list_display_links = "id", "name", "slug"
    search_fields = "name",
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """
    Админ панель модели Подкатегории товаров
    """
    list_display = "id", "category", "name", "slug"
    list_display_links = "id", "category", "name", "slug"
    search_fields = "name",
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    """
    Админ панель отображения Картинок товаров в самом товаре
    """
    model = ProductImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админ панель модели Товары
    """
    inlines = [ProductImageInline]
    list_display = "id", "image", "name", "slug", "price", "stock",  "available", "created", "updated"
    list_display_links = "name",
    list_filter = "available", "created", "updated"
    search_fields = "name",
    prepopulated_fields = {"slug": ("name",)}


class ShopAdmin(admin.ModelAdmin):
    """
    Админ панель модели Shop
    """
    list_display = ['name', 'descriptions', 'address', 'phone', 'email', 'image', 'product']


admin.site.register(Shop, ShopAdmin)
