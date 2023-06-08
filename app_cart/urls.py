from django.urls import path
from .views import add_in_comparison, list_product_in_comparison

app_name = 'app_cart'

urlpatterns = [
    path('comparison/', list_product_in_comparison, name='comparison_list'),
    path('comparison/<product_id>', add_in_comparison, name='add-in-comparison'),
]
