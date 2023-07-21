from app_catalog.models import ProductInShop
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from .services import Limit, get_product_banner, get_products_limited, get_top_products


class OneProduct(View):
    """Класс получения товара (1шт) из списка товаров ограниченного тиража  """

    products_limited_offers_all = ProductInShop.objects.filter(
        limited_product=True
    ).order_by("?")[:1]

    def product_day(self):
        """функция отображения ограниченного предложения товара с фиксацией на сутки"""
        if self.products_limited_offers_all:
            products_limited_offers = Limit().get_product_day(
                product_for_day=self.products_limited_offers_all
            )
            OneProduct.products_limited_offers_all = products_limited_offers
            return products_limited_offers


def main_page(request: HttpRequest):
    """функция главной страницы:
     top_products: популярные товары (фильтр по самым продаваемым)
     products_banners: баннеры с товарами (фильтр max кол-во на складе),
     product_day: продукт из серии ограниченного тиража, зафиксированный на сутки
     products_limited: продукты ограниченного тиража
     """
    top_products = get_top_products()
    products_banners = get_product_banner()
    product_day = OneProduct().product_day()
    products_limited = get_products_limited(product_day)

    return render(
        request,
        "app_main_page/main.jinja2",
        {
            "top_products": top_products,
            "products_limited": products_limited,
            "products_banners": products_banners,
            "limited_offers": product_day,
        },
    )
