"""
Сервисы для работы с каталогом, товарами, магазинами
"""
from django.core.paginator import Paginator
from django.http.request import QueryDict

from app_cart.services import CartServicesMixin
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

def catalog_obj_order_by(parameter: str) -> Product:
    return Product.objects.order_by(parameter)

def sort_catalog(obj: QueryDict) -> dict:
    """
    Метод сортировки каталога, плюс пагинация
    :param obj: передаваемый параметр:
        parameter - popular, price.
        date - Up, Down.
    :type obj: django.http.request.QueryDict.
    :return:
        {
        products - объект сортировки,
        sort - тэг сортировки
        }
    :rtype: dict
    """
    if obj.get("parameter"):
        parameter = obj.get("parameter")
        return {'products': catalog_obj_order_by(parameter),
                'sort': 'base'}
    if obj.get("date") == "Up":
        return {'products': catalog_obj_order_by('updated'),
                'sort': 'base'}
    if obj.get("date") == "Down":
        return {'products': catalog_obj_order_by('-updated'),
                'sort': 'price_high'}
    if obj.get('page_tag'):
        print(obj.get('page_tag'))
    if obj.get('add_card'):
        pk = int(obj.get('product'))
        cart = CartServicesMixin()
        cart.add_product_to_cart(pk)
    return {'products': Product.objects.all(),
            'sort': 'base'}

def filter_catalog(post) -> Product:
    price_filter = post.get('price').split(';')
    min_price_filter = int(price_filter[0])
    max_price_filter = int(price_filter[1])
    if post.get('stock') == 'on':
        print('good')
    if post.get('free_delivery') == 'on':
        print('free delivery')
    products = Product.objects.filter(price__gte=min_price_filter, price__lte=max_price_filter)
    return products


def paginator(obj, request):
    paginator_catalog = Paginator(obj, 2)
    page_number = request.get('page_catalog')
    if page_number is None:
        page_number = 0
    catalog_page_obj = paginator_catalog.get_page(page_number)
    return catalog_page_obj
