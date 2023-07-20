import logging
from csv import DictReader
from io import TextIOWrapper

from django.contrib import admin, messages
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import path

from .forms import ProductCSVImportForm
from .models import (
    Category,
    Comments,
    Product,
    ProductInShop,
    ProductInShopImage,
    Shop,
    Specifications,
    SubCategory,
    Subspecifications,
)

log = logging.getLogger(__name__)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админ панель модели Категории товаров
    """

    change_list_template = "admin/cache_change_list.html"
    list_display = "id", "name", "slug"
    list_display_links = "id", "name", "slug"
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    actions = ["clear_cache"]

    def category_cache_clear(self, request: HttpRequest):
        """
        функция создания кнопки удаления cache в админке category
        """
        cache.delete("category")
        messages.add_message(request, messages.INFO, "Category cache cleared")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def get_urls(self):
        """
        функция создания кнопки удаления cache в админке category
        """
        urls = super().get_urls()
        my_urls = [
            path("clear_cache", self.admin_site.admin_view(self.category_cache_clear)),
        ]
        return my_urls + urls


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """Админ панель модели Подкатегории товаров"""

    change_list_template = "admin/cache_change_list.html"
    list_display = "id", "category", "name"
    list_display_links = "id", "category", "name"
    search_fields = ("name",)
    actions = ["clear_cache"]

    def subcategory_cache_clear(self, request: HttpRequest):
        """
        функция удаления cache в админке subcategory
        """
        cache.delete("subcategory")
        messages.add_message(request, messages.INFO, "Subcategory cache cleared")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def get_urls(self):
        """
        функция создания кнопки удаления cache в админке subcategory
        """
        urls = super().get_urls()
        my_urls = [
            path(
                "clear_cache", self.admin_site.admin_view(self.subcategory_cache_clear)
            ),
        ]
        return my_urls + urls


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ панель модели Товары"""

    change_list_template = "admin/cache_change_list.html"
    list_display = "id", "image_main", "name", "created", "updated", "description"
    list_display_links = ("name",)
    list_filter = "created", "updated"
    search_fields = ("name",)
    actions = ["clear_cache"]

    def product_cache_clear(self, request: HttpRequest):
        """
        функция очистки cache модели Product
        """
        cache.delete("product")
        messages.add_message(request, messages.INFO, "Product cache cleared")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def get_urls(self):
        """
        функция создания кнопки удаления cache в админке product
        """
        urls = super().get_urls()
        my_urls = [
            path("clear_cache", self.admin_site.admin_view(self.product_cache_clear)),
        ]
        return my_urls + urls


class ProductInShopImageInline(admin.TabularInline):
    """Админ панель отображения Картинок товаров в самом товаре"""

    model = ProductInShopImage
    extra = 0


@admin.register(ProductInShop)
class ProductInShopAdmin(admin.ModelAdmin):
    """Админ панель модели Товары в магазине"""

    actions = ["clear_cache"]
    change_list_template = "admin/products_in_shop_change_list.html"
    inlines = [ProductInShopImageInline]
    list_display = (
        "id",
        "product",
        "shop",
        "quantity",
        "price",
        "available",
        "limited_product",
    )
    list_display_links = (
        "id",
        "product",
        "shop",
        "quantity",
        "price",
        "available",
        "limited_product",
    )
    list_filter = (
        "id",
        "product",
        "shop",
        "quantity",
        "price",
        "available",
        "limited_product",
    )

    def products_in_shop_cache_clear(self, request: HttpRequest):
        """
        функция очистки cache модели ProductInShop
        """
        cache.delete("product_in_shop")
        messages.add_message(request, messages.INFO, "Product In Shop cache cleared")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        """
        функция создания импорта товаров в БД модели ProductInShop
        """
        if request.method == "GET":
            form = ProductCSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/import_products_csv.html", context)
        else:
            form = ProductCSVImportForm(request.POST, request.FILES)
            if not form.is_valid():
                context = {
                    "form": form,
                }
                return render(
                    request, "admin/import_products_csv.html", context, status=400
                )

            csv_file = TextIOWrapper(
                form.files["csv_file_product"].file,
                encoding=request.encoding,
            )
            try:
                for row in DictReader(csv_file):
                    product_in_shop, created = ProductInShop.objects.get_or_create(
                        product_id=Product.objects.get(name=row["product_name"]).id,
                        shop_id=Shop.objects.get(name=row["shop_name"]).id,
                        price=row["price"],
                        quantity=row["quantity"],
                        available=row["available"],
                        limited_product=row["limited_product"],
                    )
                    if not created:
                        log.warning(
                            f"Импорт выполнен частично. Товар {product_in_shop} был импортирован ранее."
                        )
                    else:
                        if row["image"]:
                            product_id = product_in_shop.id
                            for img in row["image"].split(";"):
                                print(img)
                                (
                                    product_in_shop_image,
                                    created,
                                ) = ProductInShopImage.objects.get_or_create(
                                    product_in_shop_id=product_id, image=img
                                )
                                if not created:
                                    log.warning(
                                        f"Ошибка импорта картинки {product_in_shop_image} "
                                    )

            except Exception as error_import:
                self.message_user(request, "Импорт Завершён с ошибкой")
                log.error(f"Импорт Завершен с ошибкой: {error_import}")
            else:
                log.info("Импорт Выполнен")
                self.message_user(request, "Импорт Выполнен")
            finally:
                return redirect("..")

    def get_urls(self):
        """
        функция создания кнопок в админке product_in_shop для проведения импорта и очистки cache
        """
        urls = super(ProductInShopAdmin, self).get_urls()
        new_urls = [
            path(
                "import-products-in-shop-csv/",
                self.import_csv,
                name="import_products_in_shop_csv",
            ),
            path(
                "clear_cache",
                self.admin_site.admin_view(self.products_in_shop_cache_clear),
            ),
        ]
        return new_urls + urls


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """Админ панель модели Shop"""

    list_display = ["name", "descriptions", "address", "phone", "email", "image"]


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """Админ панель модели Comments"""

    list_display = ["product_in_shop", "comment", "user", "created", "updated"]
    list_display_links = ("comment",)


class SpecificationsInline(admin.TabularInline):
    model = Subspecifications


@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    """Админ панель модель Specifications"""

    list_display = ["id", "name_specification", "product"]
    inlines = [SpecificationsInline]


@admin.register(Subspecifications)
class SubspecificationsAdmin(admin.ModelAdmin):
    """Админ панель модель Subspecifications"""

    list_display = ["id", "specification", "text_subspecification"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "specification",
                    "name_subspecification",
                    "text_subspecification",
                ],
            },
        ),
    ]
