from django.urls import path
from .views import CheckoutOrderView, CreateOrderView

app_name = 'apporders'

urlpatterns = [
    path('checkout/', CheckoutOrderView.as_view(), name='checkout_order'),
    path('create/', CreateOrderView.as_view(), name='create_order')
]
