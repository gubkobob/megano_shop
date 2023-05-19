from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse


def settings(request):
    return render(request, 'app_administrator/settings.html')


def clear_all(request):
    cache.clear()
    return HttpResponse('the Site cache has been reset')


def clear_categories(request):
    cache.delete('categories')
    return HttpResponse('cache Сategories clearing')


def clear_subcategories(request):
    cache.delete('subcategories')
    return HttpResponse('cache Subcategories clearing')


def clear_banners(request):
    cache.delete('banners')
    return HttpResponse('cache Banners clearing')


def clear_shops(request):
    cache.delete('shops')
    return HttpResponse('cache Shops clearing')


def clear_products(request):
    cache.delete('products')
    return HttpResponse('cache Products clearing')
