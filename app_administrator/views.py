from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse
from app_administrator.signals import my_signal
from app_catalog.models import Category, SubCategory, Product


def settings(request):
    if request.user.is_superuser:
        return render(request, 'app_administrator/settings.html')
    else:
        return HttpResponse('Ошибка 404 или Not Found')


def clear_all(request):
    if request.user.is_superuser:
        cache.clear()
        return HttpResponse('the Site cache has been reset')
    else:
        return HttpResponse('Ошибка 404 или Not Found')


def clear_categories(request):
    if request.user.is_superuser:
        model = ''
        if model == Category:
            my_signal.send(sender=Category)
        elif model == SubCategory:
            my_signal.send(sender=SubCategory)
        elif model == Product:
            my_signal.send(sender=Product)
        return HttpResponse('cache Model', model)
    else:
        return HttpResponse('Ошибка 404 или Not Found')
