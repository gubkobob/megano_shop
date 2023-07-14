from django.urls import path
from .views import (
    add_in_comparison,
    list_product_in_comparison,
    remove_product_in_comparison, cart_detail, cart_add, cart_remove,
    coupon_apply,
)

app_name = 'app_cart'

urlpatterns = [
    path('comparison/', list_product_in_comparison, name='comparison_list'),
    path('comparison/<product_id>/add', add_in_comparison, name='add_in_comparison'),
    path('comparison/<product_id>/remove', remove_product_in_comparison, name='remove_product_in_comparison'),
    path('coupon/apply', coupon_apply, name='coupon_apply'),
    path("", cart_detail, name='cart_detail'),
    path("add/<int:product_in_shop_id>/", cart_add, name='cart_add'),
    path("remove/<int:product_in_shop_id>/", cart_remove, name='cart_remove'),
]
