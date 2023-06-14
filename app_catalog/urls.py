from django.urls import path
from .views import *

app_name = 'appcatalog'

urlpatterns = [
    path('', CategoryView.as_view(), name='catalog'),
    path('product_details/<int:pk>/', ProductCartDetailView.as_view(), name='product_details')
]
