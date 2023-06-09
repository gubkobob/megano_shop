from django.db.models import Sum
from django.views import View
from datetime import datetime
from app_catalog.models import Product
from app_administrator.models import SettingsModel


class MainPage(View):
    """ Класс ограниченного предложения товара (1шт) """
    products_limited_offers_all = Product.objects.filter(limited_product=True)
    products_limited_offers = products_limited_offers_all
    start_time = datetime.now()
    print('время старта программы', start_time)

    def get_product_day(self):
        """функция отображения ограниченного предложения товара с фиксацией на сутки"""
        now_time = datetime.now()
        time_difference = int((now_time - self.start_time).total_seconds())
        print('Прошло', time_difference, "sec")
        if time_difference < 5:
            return self.products_limited_offers
        else:
            MainPage.products_limited_offers = Product.objects.filter(limited_product=True).order_by('?')[:1]
            MainPage.start_time = datetime.now()
            return MainPage.products_limited_offers


def get_product_banner():
    """функция отображения баннеров на главной"""
    value_products_banner = getattr(SettingsModel.objects.first(), 'products_banner')
    products_banners = Product.objects.all().order_by('-price')[:value_products_banner]
    return products_banners


def get_products_limited():
    """функция отображения товаров ограниченного тиража на главной"""
    value_limited_edition_products = getattr(SettingsModel.objects.first(), 'limited_edition_products')
    products_limited = Product.objects.filter(limited_product=True)[:value_limited_edition_products]
    return products_limited


def get_top_products():
    """функция отображения популярных товаров на главной"""
    # top_products = Product.objects.annotate(quantity_sum=Sum('order_items__quantity')).order_by('-quantity_sum')[:8]
    value_popular_products = getattr(SettingsModel.objects.first(), 'popular_products')
    top_products = Product.objects.all().order_by('-price')[:value_popular_products]
    return top_products
