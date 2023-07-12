"""
Сервисы для работы с каталогом, товарами, магазинами
"""
from django.core.paginator import Paginator
from django.db.models import Count
from django.http.request import QueryDict

from app_cart.services import CartServicesMixin
from .models import ProductInShop
from app_discounts.models import Discount



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

def catalog_obj_order_by(parameter: str, flag: str = None) -> ProductInShop:
    print(parameter)
    if parameter == 'comments':
        return ProductInShop.objects.annotate(num_parametr=Count('comments')).order_by('-num_parametr')
    if parameter == 'subcategory':
        return ProductInShop.objects.filter(product__subcategory__name=flag)
    if parameter == 'category':
        return ProductInShop.objects.filter(product__category__name=flag)
    return ProductInShop.objects.order_by(f'{parameter}')

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
    # print(obj.get("parameter"))
    if obj.get("parameter"):
        parameter = obj.get("parameter")
        flag = obj.get("flag")
        sort = 'base' if parameter != '-product__created' else 'price_high'
        return {'productsinshops': catalog_obj_order_by(parameter, flag),
                # 'discount': Discount.objects.all(),
                'sort': sort}
    # if obj.get('page_tag'):
    #     print(obj.get('page_tag'))
    if obj.get('add_card'):
        pk = int(obj.get('product'))
        cart = CartServicesMixin()
        cart.add_product_to_cart(pk)
    return {'productsinshops': ProductInShop.objects.all(),
            # 'discount': Discount.objects.all(),
            'sort': 'base'}

def filter_catalog(post) -> ProductInShop:
    price_filter = post.get('price').split(';')
    min_price_filter = int(price_filter[0])
    max_price_filter = int(price_filter[1])
    if post.get('stock') == 'on':
        print('good')
    if post.get('free_delivery') == 'on':
        print('free delivery')
    pis = ProductInShop.objects.filter(price__gte=min_price_filter, price__lte=max_price_filter)
    return pis


def paginator(obj, request):
    paginator_catalog = Paginator(obj, 4)
    page_number = request.get('page_catalog')
    if page_number is None:
        page_number = 1
    catalog_page_obj = paginator_catalog.get_page(page_number)
    return catalog_page_obj
