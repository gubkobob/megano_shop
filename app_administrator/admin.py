from django.contrib import admin, messages
from django.core.cache import cache
from django.urls import path
from django.http import HttpResponseRedirect, HttpRequest
from .models import SettingsModel


@admin.register(SettingsModel)
class SettingsModelAdmin(admin.ModelAdmin):
    """Админ панель модели Настроек """
    list_display = 'id', 'limited_edition_products', 'hot_offers', 'popular_products', 'products_banner', \
                   'viewed_products', 'selected_categories', 'cache_time'
    list_display_links = 'id', 'limited_edition_products', 'hot_offers', 'popular_products', 'products_banner', \
                         'viewed_products', 'selected_categories', 'cache_time'
    search_fields = 'id', 'limited_edition_products', 'hot_offers', 'popular_products', 'products_banner', \
                    'viewed_products', 'selected_categories', 'cache_time'

    def has_add_permission(self, request: HttpRequest):
        return False

    def has_delete_permission(self, request: HttpRequest, obj=None):
        return False

    def all_cache_clear(self, request: HttpRequest):
        cache.clear()
        messages.add_message(request, messages.INFO, 'ALL cache cleared')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('clear_cache', self.admin_site.admin_view(self.all_cache_clear)),
        ]
        return my_urls + urls
