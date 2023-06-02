from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse


def settings(request):
    if request.user.is_superuser:
        return render(request, 'app_administrator/administrator.jinja2')
    else:
        return HttpResponse('Ошибка 404 или Not Found')


def clear_all(request):
    if request.user.is_superuser:
        cache.clear()
        return HttpResponse('the Site cache has been reset')
    else:
        return HttpResponse('Ошибка 404 или Not Found')


def clear_category(request):
    if request.user.is_superuser:
        cache.delete('categories')
        return HttpResponse('the category cache has been reset')
    else:
        return HttpResponse('Ошибка 404 или Not Found')


def clear_subcategory(request):
    if request.user.is_superuser:
        cache.delete('subcategories')
        return HttpResponse('the subcategory cache has been reset')
    else:
        return HttpResponse('Ошибка 404 или Not Found')


def clear_product(request):
    if request.user.is_superuser:
        cache.delete('products')
        return HttpResponse('the product cache has been reset')
    else:
        return HttpResponse('Ошибка 404 или Not Found')
