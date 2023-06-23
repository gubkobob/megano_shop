from django.db.models import Sum
from datetime import datetime
from app_administrator.models import SettingsModel
from django.db.models import Min
from app_catalog.models import Product, ProductInShop


class Limit:
    """ Класс смены товара дня через определенный промежуток времени """
    start_time = datetime.now().replace(hour=00, minute=00, second=10, microsecond=0)

    def get_product_day(self, my_product):
        """функция смены товара дня через определенный промежуток времени"""
        now_time = datetime.now()
        time_difference = int((now_time - self.start_time).total_seconds())

        if 0 < time_difference < 86400:
            return my_product
        else:
            if ProductInShop.objects.filter(limited_product=True).order_by('?')[:1]:
                products_limited_offers = ProductInShop.objects.filter(limited_product=True).order_by('?')[:1]
                Limit.start_time = datetime.now().replace(hour=00, minute=00, second=10, microsecond=0)
                return products_limited_offers


def get_product_banner():
    """функция отображения баннеров на главной"""
    value_products_banner = getattr(SettingsModel.objects.first(), 'products_banner')
    products_banners = Product.objects.all().order_by('name')[:value_products_banner]
    return products_banners


def get_products_limited(product_day):
    """функция отображения товаров ограниченного тиража на главной"""
    if product_day:
        value_limited_edition_products = getattr(SettingsModel.objects.first(), 'limited_edition_products')
        products_limited = ProductInShop.objects.filter(limited_product=True)[:value_limited_edition_products]
        return products_limited


def get_top_products():
    """функция отображения популярных товаров на главной"""
    # top_products = Product.objects.annotate(quantity_sum=Sum('order_items__quantity')).order_by('-quantity_sum')[:8]
    value_popular_products = getattr(SettingsModel.objects.first(), 'popular_products')
    top_products = Product.objects.values('name', 'category', 'subcategory').annotate(
        min_price=Min('products_in_shop__price')).filter(min_price__isnull=False).order_by('min_price')[:value_popular_products]
    # top_products = Product.objects.all().order_by('name')[:value_popular_products]
    return top_products
