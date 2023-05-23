from django.urls import path
from .views import (settings,
                    clear_all,
                    clear_section,
                    )
from .views import settings, clear_all

app_name = 'appadministrator'

urlpatterns = [
    path('', settings, name='settings'),
    path('clear_cache_all/', clear_all, name='clear_all'),
    path('clear_cache_section/', clear_section, name='clear_section'),
]
