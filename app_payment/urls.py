from django.urls import path
from .views import PayView

app_name = 'apppayment'

urlpatterns = [
    path('', PayView.as_view(), name='payment'),
]
