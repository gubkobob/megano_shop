from django.contrib import admin, messages
from django.core.cache import cache
from django.urls import path
from django.http import HttpResponseRedirect, HttpRequest

from .models import Category, SubCategory, Product, Shop, ProductImage, Specifications, Subspecifications


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ панель модели Категории товаров"""
    list_display = "id", "name"
    list_display_links = "id", "name"
    search_fields = "name",
    prepopulated_fields = {"slug": ("name",)}
    actions = ['clear_cache']

    def category_cache_clear(self, request: HttpRequest):
        cache.delete('categories')
        messages.add_message(request, messages.INFO, 'Category cache cleared')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('clear_cache', self.admin_site.admin_view(self.category_cache_clear)),
        ]
        return my_urls + urls


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """Админ панель модели Подкатегории товаров"""
    list_display = "id", "category", "name"
    list_display_links = "id", "category", "name"
    search_fields = "name",

    def subcategory_cache_clear(self, request: HttpRequest):
        cache.delete('subcategories')
        messages.add_message(request, messages.INFO, 'Subcategory cache cleared')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('clear_cache', self.admin_site.admin_view(self.subcategory_cache_clear)),
        ]
        return my_urls + urls


class ProductImageInline(admin.TabularInline):
    """Админ панель отображения Картинок товаров в самом товаре"""
    model = ProductImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ панель модели Товары"""
    inlines = [ProductImageInline]
    list_display = "id", "image", "name", "slug", "price", "stock",  "available", \
                   "created", "updated", "limited_product"
    list_display_links = "name",
    list_filter = "available", "created", "updated"
    search_fields = "name",
    prepopulated_fields = {"slug": ("name",)}

    def product_cache_clear(self, request: HttpRequest):
        cache.delete('products')
        messages.add_message(request, messages.INFO, 'Product cache cleared')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('clear_cache', self.admin_site.admin_view(self.product_cache_clear)),
        ]
        return my_urls + urls


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """Админ панель модели Shop"""
    list_display = ['name', 'descriptions', 'address', 'phone', 'email', 'image']


class SpecificationsInline(admin.TabularInline):
    model = Subspecifications


@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    """Админ панель модель Specifications"""
    list_display = ['id', 'name_specification', 'product']
    inlines = [SpecificationsInline]


@admin.register(Subspecifications)
class SubspecificationsAdmin(admin.ModelAdmin):
    """Админ панель модель Subspecifications"""
    list_display = ['id', 'specification', 'text_subspecification']
    fieldsets = [
        (
            None,
            {
                "fields": ['specification', "name_subspecification", 'text_subspecification'],
            },
        ),
    ]
