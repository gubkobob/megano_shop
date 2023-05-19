from django.urls import path
from .views import (settings,
                    clear_all,
                    clear_categories,
                    clear_subcategories,
                    clear_banners,
                    clear_shops,
                    clear_products
                    )

app_name = 'appadministrator'

urlpatterns = [
    path('', settings, name='settings'),
    path('clear_cache_all/', clear_all, name='clear_all'),
    path('clear_cache_categories/', clear_categories, name='clear_categories'),
    path('clear_cache_subcategories/', clear_subcategories, name='clear_subcategories'),
    path('clear_cache_banners/', clear_banners, name='clear_banners'),
    path('clear_cache_shops/', clear_shops, name='clear_shops'),
    path('clear_cache_products/', clear_products, name='clear_products'),
]
