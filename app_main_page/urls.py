from django.urls import path

from .views import main_page

app_name = "appmainpage"

urlpatterns = [
    path("", main_page, name="main_page"),
]
