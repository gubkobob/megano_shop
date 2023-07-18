from django.urls import path

from .views import DiscountView

app_name = "appdiscount"

urlpatterns = [
    path("", DiscountView.as_view(), name="sale"),
]
