from io import TextIOWrapper
from csv import DictReader

from django.contrib import admin, messages
from django.core.cache import cache
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse

from .forms import CSVImportForm
from .models import Category, SubCategory, Product, Shop, ProductInShopImage, Specifications, Subspecifications, \
    ProductInShop, Comments


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


@admin.register(ProductInShop)
class ProductInShopAdmin(admin.ModelAdmin):
    """Админ панель модели Товары в магазине"""
    change_list_template = 'admin/products_in_shop_change_list.html'
    inlines = [ProductInShopImageInline]
    list_display = "id", "product", "shop", "quantity", "price", "available", "limited_product"
    list_display_links = "product", "shop", "quantity", "price", "available", "limited_product"
    list_filter = "product", "shop", "quantity", "price", "available", "limited_product"

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context)
        else:
            form = CSVImportForm(request.POST, request.FILES)
            if not form.is_valid():
                context = {
                    "form": form,
                }
                return render(request, 'admin/csv_form.html', context, status=400)

            csv_file = TextIOWrapper(
                form.files['csv_file'].file,
                encoding=request.encoding,
            )
            reader = DictReader(csv_file)
            for row in reader:
                products_in_shop = ProductInShop.objects.get_or_create(
                    price=row['price'],
                    quantity=row['quantity'],
                    product=ProductInShop.product.get_or_create(name=row['product']),
                    shop=Shop.objects.get_or_create(id=row['shop']),
                    available=row['available'],
                    limited_product=row['limited_product']
                )

                ProductInShop.objects.bulk_create(products_in_shop)
            self.message_user(request, "Data from CSV was imported")
            return redirect("..")

    def get_urls(self):
        urls = super(ProductInShopAdmin, self).get_urls()
        new_urls = [
            path(
                'import-products-in-shop-csv/',
                self.import_csv,
                name='import_products_in_shop_csv',
            ),
        ]
        return new_urls + urls


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ панель модели Товары"""
    list_display = "id", "image_main", "name", "created", "updated", "description"
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


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """Админ панель модели Shop"""
    list_display = ['name', 'descriptions', 'address', 'phone', 'email', 'image']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """Админ панель модели Comments"""
    list_display = ['product_in_shop', 'comment', 'user', 'created', 'updated']
    list_display_links = "comment",


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
