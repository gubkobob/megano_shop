from django.contrib import admin
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "id", "name", "slug"
    list_display_links = "id", "name", "slug"
    search_fields = "name",
    prepopulated_fields = {"slug": ("name",)}

# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 0

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = "id", "image", "name", "slug", "price", "stock",  "available", "created", "updated"
#     list_display_links = "name",
#     list_filter = "available", "created", "updated"
#     search_fields = "name",
#     prepopulated_fields = {"slug": ("name",)}
#     inlines = [ProductImageInline]
#
#
#
# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = "id", "product", "image"
#     list_display_links = "id", "product", "image"
