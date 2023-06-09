from django.shortcuts import render
from django.db.models import Sum
from .services import MainPage, get_product_banner, get_products_limited, get_top_products


def main_page(request):
    """функция главной страницы"""
    top_products = get_top_products()
    products_banners = get_product_banner()
    products_limited = get_products_limited()
    product_day = MainPage().get_product_day()

    return render(request, 'app_main_page/main.jinja2', {
        'top_products': top_products,
        'products_limited': products_limited,
        'products_banners': products_banners,
        'limited_offers': product_day
    })





