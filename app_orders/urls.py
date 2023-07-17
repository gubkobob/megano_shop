from django.urls import path

from .views import CreateOrderView, OrderDetailView, OrdersListView

app_name = "apporders"

urlpatterns = [
    path("create/", CreateOrderView.as_view(), name="create_order"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path("history/", OrdersListView.as_view(), name="orders_history"),
]
