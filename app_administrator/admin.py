from django.contrib import admin
from  .models import SettingsModel


@admin.register(SettingsModel)
class SettingsModelAdmin(admin.ModelAdmin):
    """Админ панель модели Настроек """
    list_display = "id", "limited_edition_products", "popular_products", "products_banner"
    list_display_links = "id", "limited_edition_products", "popular_products", "products_banner"
    search_fields = "limited_edition_products", "popular_products", "products_banner"
