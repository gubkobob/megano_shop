from django.contrib import admin, messages
from django.core.cache import cache
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import path

from .models import SettingsModel


@admin.register(SettingsModel)
class SettingsModelAdmin(admin.ModelAdmin):
    """Админ панель модели Настроек"""

    change_list_template = "admin/cache_all_change_list.html"
    list_display = (
        "id",
        "limited_edition_products",
        "hot_offers",
        "popular_products",
        "products_banner",
        "count_viewed",
        "selected_categories",
        "cache_time",
        "price_express_delivery",
        "price_ordinary_delivery",
        "min_total_price_order",
    )
    list_display_links = (
        "id",
        "limited_edition_products",
        "hot_offers",
        "popular_products",
        "products_banner",
        "count_viewed",
        "selected_categories",
        "cache_time",
        "price_express_delivery",
        "price_ordinary_delivery",
        "min_total_price_order",
    )
    search_fields = (
        "id",
        "limited_edition_products",
        "hot_offers",
        "popular_products",
        "products_banner",
        "count_viewed",
        "selected_categories",
        "cache_time",
        "price_express_delivery",
        "price_ordinary_delivery",
        "min_total_price_order",
    )

    def has_add_permission(self, request: HttpRequest):
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None):
        return False

    def all_cache_clear(self, request: HttpRequest):
        cache.clear()
        messages.add_message(request, messages.INFO, "ALL cache cleared")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("clear_cache", self.admin_site.admin_view(self.all_cache_clear)),
        ]
        return my_urls + urls
