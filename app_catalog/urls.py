from django.urls import path
from .views import CategoryView, ProductCartDetailView

app_name = 'appcatalog'

urlpatterns = [
    path('', CategoryView.as_view(), name='catalog'),
    path('product_details/<int:pk>/', ProductCartDetailView.as_view(), name='product_details')
]
