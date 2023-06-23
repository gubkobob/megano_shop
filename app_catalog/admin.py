from django.contrib import admin, messages
from django.core.cache import cache
from django.urls import path
from django.http import HttpResponseRedirect, HttpRequest

from .models import Category, SubCategory, Product, ProductInShop, Shop, Specifications, \
    Subspecifications, ProductInShopImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админ панель модели Категории товаров
    """
    list_display = "id", "name", "slug"
    list_display_links = "id", "name", "slug"
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


class ProductInShopImageInline(admin.TabularInline):
    """Админ панель отображения Картинок товаров в самом товаре"""
    model = ProductInShopImage
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ панель модели Товары"""
    list_display = "id", "image_main", "name", "slug", "created", "updated", "description"
    list_display_links = "name",
    list_filter = "created", "updated"
    search_fields = "name",

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


@admin.register(ProductInShop)
class ProductInShopAdmin(admin.ModelAdmin):
    inlines = [ProductInShopImageInline]
    list_display = "id", "product", "shop", "quantity", "price", "available", "limited_product", "last_visit"
    list_display_links = "product", "shop", "quantity", "price", "available", "limited_product", "last_visit"
    list_filter = "product", "shop", "quantity", "price", "available", "limited_product", "last_visit"


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
