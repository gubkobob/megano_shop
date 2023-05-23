from .models import ContextProcessorsModel
from app_catalog.models import Product



def set_limited_edition_products(request):
    return {'limited_products' : ContextProcessorsModel.limited_edition_products}

def set_limited_edition_products(request):
    limited_products = Product.objects.filter('stock')[int:(ContextProcessorsModel.limited_edition_products)]
    return {'limited_products': limited_products}


def set_hot_offers(request):
    return {'limited__hot_offers': ContextProcessorsModel.hot_offers}


def set_popular_products(request):
    return {'limited_popular_products': ContextProcessorsModel.popular_products}


def set_products_day(request):
    return {'limited_products_day': ContextProcessorsModel.products_day}


def set_banners(request):
    return {'limited_banners': ContextProcessorsModel.banners}


def set_viewed_products(request):
    return {'limited_viewed_products': ContextProcessorsModel.viewed_products}


def set_selected_categories(request):
    return {'limited_selected_categories': ContextProcessorsModel.selected_categories}


def set_cache_time(request):
    return {'cache_time': ContextProcessorsModel.cache_time}
