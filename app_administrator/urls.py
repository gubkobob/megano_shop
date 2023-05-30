from django.urls import path
from .views import settings, clear_all

app_name = 'appadministrator'

urlpatterns = [
    path('', settings, name='settings'),
    path('clear_cache_all/', clear_all, name='clear_all'),
]
