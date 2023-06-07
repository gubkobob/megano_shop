"""
Сервисы для работы с каталогом, товарами, магазинами
"""
from django.core.paginator import Paginator
from .models import Product



class ProductServicesMixin:
    """
    Класс - примесь для использования сервисов для работы с товарами
    """

    def add_review_to_product(self):
        """
        функция добавления отзыва к товару
        """

    def get_viewed_products_history(self):
        """
        функция получения списка просмотренных товаров
        """

    def add_viewed_products_history(self):
        """
        функция добавления товара к списку просмотренных
        """

    def get_viewed_products_history(self):
        """
        функция получения списка просмотренных товаров
        """

    def get_list_comments_on_products(self) -> list[str]:
        """
        функция получения списка комментариев к продукту
        """

    def get_discount_on_products(self):
        """
        функция получения скидки к продукту
        """

    def get_quantity_comments_on_products(self) -> int:
        """
        функция получения количество комментариев к продукту
        """


class ShopServicesMixin:
    """
    Класс - примесь для использования сервисов для работы с магазинами
    """


def sort_catalog(obj) -> dict:
    if obj.get("price") == "True":
        return {'products': Product.objects.order_by('price'),
                'sort': 'base'}
    if obj.get("date") == "Up":
        return {'products': Product.objects.order_by('updated'),
                'sort': 'base'}
    if obj.get("date") == "Down":
        return {'products': Product.objects.order_by('-updated'),
                'sort': 'price_high'}
    return {'products': Product.objects.all(),
            'sort': 'base'}

def paginator(obj, request):
    paginator_catalog = Paginator(obj, 2)
    page_number = request.get('page_catalog')
    if page_number is None:
        page_number = 0
    catalog_page_obj = paginator_catalog.get_page(page_number)
    return catalog_page_obj
