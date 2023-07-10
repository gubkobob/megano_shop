from django.urls import path
from .views import CheckoutOrderView, CreateOrderView, OrderDetailView, OrdersListView

app_name = 'apporders'

urlpatterns = [
    path('checkout/', CheckoutOrderView.as_view(), name='checkout_order'),
    path('create/', CreateOrderView.as_view(), name='create_order'),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path('history/', OrdersListView.as_view(), name='orders_history'),
]
