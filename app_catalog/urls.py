from django.urls import path
from .views import CategoryView, product_details

app_name = 'appcatalog'

urlpatterns = [
    path('', CategoryView.as_view(), name='catalog'),
    path('product_details/<int:pk>/', product_details, name='product_details')
]
