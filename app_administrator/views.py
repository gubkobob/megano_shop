from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import UpdateView
from .models import SettingsModel
from .forms import SettingsForm


def get_settings(request):
    if request.user.is_superuser:
        settings_page = SettingsModel.objects.all()
        return render(request, 'app_administrator/administrator.jinja2', {'settings': settings_page})
    else:
        return HttpResponse('Ошибка 404 или Not Found')


def cache_settings(request):
    if request.user.is_superuser:
        return render(request, 'app_administrator/administrator_cache.jinja2')
    else:
        return HttpResponse('Ошибка 404 или Not Found')


def create_settings(request):
    if request.user.is_superuser:
        error = ''
        if request.method == 'POST':
            form = SettingsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('appadministrator/settings')
            else:
                error = 'Форма была неверной'
        form = SettingsForm()
        data = {
            'form': form,
            'error': error
        }
        return render(request, 'app_administrator/administrator_update.jinja2', data)
    else:
        return HttpResponse('Ошибка 404 или Not Found')


class SettingsUpdateView(UpdateView):
    model = SettingsModel
    template_name = 'app_administrator/administrator_update.jinja2'
    fields = ['limited_edition_products', 'hot_offers', 'popular_products', 'products_banner', 'viewed_products',
              'selected_categories', 'cache_time']
