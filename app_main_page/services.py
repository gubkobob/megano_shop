from django.db.models import Sum
from datetime import datetime
from app_administrator.models import SettingsModel
from app_catalog.models import Product


class Limit:
    """ Класс смены товара дня через определенный промежуток времени """
    start_time = datetime.now().replace(hour=00, minute=00, second=10, microsecond=0)

    def get_product_day(self, my_product):
        """функция смены товара дня через определенный промежуток времени"""
        pass
        # now_time = datetime.now()
        # time_difference = int((now_time - self.start_time).total_seconds())
        #
        # if 0 < time_difference < 86400:
        #     return my_product
        # else:
        #     if Product.objects.filter(limited_product=True).order_by('?')[:1]:
        #         products_limited_offers = Product.objects.filter(limited_product=True).order_by('?')[:1]
        #         Limit.start_time = datetime.now().replace(hour=00, minute=00, second=10, microsecond=0)
        #         return products_limited_offers


def get_product_banner():
    """функция отображения баннеров на главной"""
    pass
    # value_products_banner = getattr(SettingsModel.objects.first(), 'products_banner')
    # products_banners = Product.objects.all().order_by('-price')[:value_products_banner]
    # return products_banners


def get_products_limited(product_day):
    """функция отображения товаров ограниченного тиража на главной"""
    pass
    # if product_day:
    #     value_limited_edition_products = getattr(SettingsModel.objects.first(), 'limited_edition_products')
    #     products_limited = Product.objects.filter(limited_product=True).exclude(name=product_day[0])[
    #                        :value_limited_edition_products]
    #     return products_limited


def get_top_products():
    """функция отображения популярных товаров на главной"""
    pass
    # top_products = Product.objects.annotate(quantity_sum=Sum('order_items__quantity')).order_by('-quantity_sum')[:8]
    # value_popular_products = getattr(SettingsModel.objects.first(), 'popular_products')
    # top_products = Product.objects.all().order_by('-price')[:value_popular_products]
    # return top_products
