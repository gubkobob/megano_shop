from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse


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
