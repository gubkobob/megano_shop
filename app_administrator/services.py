from django.http import HttpResponse
from django.shortcuts import render
from django.core.cache import cache



"""
Сервисы для работы с административными настройками
"""


class AdminSettingsServicesMixin:
    """
    Класс - примесь для использования сервисов для работы с административными настройками
    """

    def get_admin_settings(self):
        """
        функция получения административных настроек
        """

    def post_admin_settings(self):
        """
        функция изменения административных настроек
        """


def clear_all(request):
    if request.user.is_superuser:
        cache.clear()
        return render(request, 'app_administrator/administrator_cache.jinja2')
    else:
        return HttpResponse('Ошибка 404 или Not Found')


def clear_category(request):
    if request.user.is_superuser:
        cache.delete('categories')
        return render(request, 'app_administrator/administrator_cache.jinja2')
    else:
        return HttpResponse('Ошибка 404 или Not Found')


def clear_subcategory(request):
    if request.user.is_superuser:
        cache.delete('subcategories')
        return render(request, 'app_administrator/administrator_cache.jinja2')
    else:
        return HttpResponse('Ошибка 404 или Not Found')


def clear_product(request):
    if request.user.is_superuser:
        cache.delete('products')
        return render(request, 'app_administrator/administrator_cache.jinja2')
    else:
        return HttpResponse('Ошибка 404 или Not Found')
