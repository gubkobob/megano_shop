from django.urls import path
from .views import add_in_comparison, list_product_in_comparison, remove_product_in_comparison

app_name = 'app_cart'

urlpatterns = [
    path('comparison/', list_product_in_comparison, name='comparison_list'),
    path('comparison/<product_id>/add', add_in_comparison, name='add_in_comparison'),
    path('comparison/<product_id>/remove', remove_product_in_comparison, name='remove_product_in_comparison'),
    # path('comparison/items', get_len_goods_to_in_comparison, name='get_len_goods_to_in_comparison'),
]
