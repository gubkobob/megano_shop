from django.urls import path
from .views import *

# app_name = 'appcatalog'

urlpatterns = [
    # path('', categories_list, name='categories_list'),
    # path('<category_slug>/', categories_list, name='categories_list_with_products'),
    # path('<category_slug>/<subcategory_slug>/', categories_list, name='subcategories_list_with_products')
    path('', CategoryView.as_view(), name='catalog'),
]
