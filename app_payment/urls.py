from django.urls import path

from .views import PayView

app_name = "apppayment"

urlpatterns = [
    path("<int:pk>/", PayView.as_view(), name="payment"),
]
