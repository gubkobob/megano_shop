from django.urls import path
from .views import categories_list

app_name = 'appcatalog'

urlpatterns = [
    path('', categories_list, name='product_list'),
    path('<category_slug>/', categories_list, name='categories_list')
]