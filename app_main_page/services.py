from datetime import datetime

from app_administrator.models import SettingsModel
from app_catalog.models import ProductInShop
from django.db.models import Sum


class Limit:
    """Класс смены товара дня через определенный промежуток времени"""

    start_time = datetime.now().replace(hour=00, minute=00, second=10, microsecond=0)

    def get_product_day(self, product_for_day):
        """функция смены товара дня через определенный промежуток времени"""
        now_time = datetime.now()
        time_difference = int((now_time - self.start_time).total_seconds())

        if 0 < time_difference < 86400:
            return product_for_day
        else:
            if ProductInShop.objects.filter(limited_product=True).order_by("?")[:1]:
                products_limited_offers = ProductInShop.objects.filter(
                    limited_product=True
                ).order_by("?")[:1]
                Limit.start_time = datetime.now().replace(
                    hour=00, minute=00, second=10, microsecond=0
                )
                return products_limited_offers


def get_product_banner():
    """функция отображения баннеров на главной"""
    value_products_banner = getattr(SettingsModel.objects.first(), "products_banner")
    products_banners = ProductInShop.objects.all().order_by("-quantity")[
        :value_products_banner
    ]
    return products_banners


def get_products_limited(product_day):
    """функция отображения товаров ограниченного тиража на главной"""
    if product_day:
        for item_product_day in product_day:
            value_limited_edition_products = getattr(
                SettingsModel.objects.first(), "limited_edition_products"
            )
            products_limited = ProductInShop.objects.filter(
                limited_product=True
            ).exclude(id=item_product_day.id)[:value_limited_edition_products]
            return products_limited


def get_top_products():
    """функция отображения популярных товаров на главной (фильтр от наиболее продаваемых)"""
    value_popular_products = getattr(SettingsModel.objects.first(), "popular_products")
    top_products = ProductInShop.objects.annotate(
        quantity_sum=Sum("order_items__quantity")
    ).order_by("-quantity_sum")[:value_popular_products]
    return top_products
