from django.urls import path
from .services import clear_all, clear_category, clear_subcategory, clear_product
from .views import get_settings, cache_settings, create_settings, SettingsUpdateView

app_name = 'appadministrator'

urlpatterns = [
    path('', get_settings, name='settings'),
    path('create/', create_settings, name='settings_create'),
    path('<int:pk>/update/', SettingsUpdateView.as_view(), name='settings_update'),
    path('cache/', cache_settings, name='cache_settings'),
    path('cache/clear_all/', clear_all, name='clear_all'),
    path('cache/clear_category/', clear_category, name='clear_category'),
    path('cache/clear_subcategory/', clear_subcategory, name='clear_subcategory'),
    path('cache/clear_product/', clear_product, name='clear_product'),
]
