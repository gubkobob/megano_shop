from django.urls import path
from .views import settings, clear_all, clear_category, clear_subcategory, clear_product

app_name = 'appadministrator'

urlpatterns = [
    path('', settings, name='settings'),
    path('clear_cache_all/', clear_all, name='clear_all'),
    path('clear_cache_category/', clear_category, name='clear_category'),
    path('clear_cache_subcategory/', clear_subcategory, name='clear_subcategory'),
    path('clear_cache_product/', clear_product, name='clear_product'),
]
