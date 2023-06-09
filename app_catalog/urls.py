from django.urls import path
from .views import categories_list, ProductCartDetailView

app_name = 'appcatalog'

urlpatterns = [
    path('', categories_list, name='categories_list'),
    path('<category_slug>/', categories_list, name='categories_list_with_products'),
    path('<category_slug>/<subcategory_slug>/', categories_list, name='subcategories_list_with_products'),
    path('product_details/<int:pk>/', ProductCartDetailView.as_view(), name='product_details')
]
