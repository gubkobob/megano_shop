from django import forms
from .models import SettingsModel
from django.forms import ModelForm, TextInput


class SettingsForm(ModelForm):
    class Meta:
        model = SettingsModel
        fields = ['limited_edition_products', 'hot_offers', 'popular_products', 'products_banner', 'viewed_products',
                  'selected_categories', 'cache_time']

        widgets = {
            'limited_edition_products': TextInput(attrs={'type': 'number', 'min_value': 1, 'max_value': 16,
                                                         'placeholder': 'Товары ограниченного тиража'}),
            'hot_offers': TextInput(attrs={'type': 'number', 'min_value': 1, 'max_value': 9,
                                           'placeholder': 'Горячие предложения'}),
            'popular_products': TextInput(attrs={'type': 'number', 'min_value': 1, 'max_value': 8,
                                                 'placeholder': 'Популярные товары'}),
            'products_banner': TextInput(attrs={'type': 'number', 'min_value': 1, 'max_value': 3,
                                                'placeholder': 'Баннеры на главной'}),
            'viewed_products': TextInput(attrs={'type': 'number', 'min_value': 1, 'max_value': 10,
                                                'placeholder': 'Просмотренные товары'}),
            'selected_categories': TextInput(attrs={'type': 'number', 'min_value': 1, 'max_value': 3,
                                                    'placeholder': 'Избранные категории'}),
            'cache_time': TextInput(attrs={'type': 'number', 'min_value': 1, 'max_value': 86400,
                                           'placeholder': 'Время обновления кэша'}),
        }
