"""
Сервисы для работы с каталогом, товарами, магазинами
"""

from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.http.request import QueryDict

from .models import ProductInShop


def catalog_obj_order_by(parameter: str, flag: str = None) -> ProductInShop:
    if parameter == "popular":
        return ProductInShop.objects.annotate(
            num_parametr=Sum("order_items__quantity")
        ).order_by("-num_parametr")
    if parameter == "-popular":
        return ProductInShop.objects.annotate(
            num_parametr=Sum("order_items__quantity")
        ).order_by("num_parametr")
    if parameter == "comments":
        return ProductInShop.objects.annotate(num_parametr=Count("comments")).order_by(
            "-num_parametr"
        )
    if parameter == "subcategory":
        return ProductInShop.objects.filter(product__subcategory__name=flag)
    if parameter == "category":
        return ProductInShop.objects.filter(product__category__name=flag)
    return ProductInShop.objects.order_by(f"{parameter}")


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
        sort_price = "base" if parameter != "-product__created" else "price_high"
        sort_popular = "base" if parameter != "-popular" else "popular_high"
        return {
            "productsinshops": catalog_obj_order_by(parameter, flag),
            "sort_price": sort_price,
            "sort_popular": sort_popular,
        }
    # if obj.get('page_tag'):
    #     print(obj.get('page_tag'))
    if obj.get("add_card"):
        pk = int(obj.get("product"))
        cart = CartServicesMixin()
        cart.add_product_to_cart(pk)
    return {
        "productsinshops": ProductInShop.objects.all(),
        "sort_price": "base",
        "sort_popular": "base",
    }


def filter_catalog(post) -> ProductInShop:
    if post.get("query"):
        return ProductInShop.objects.filter(product__name=post.get("query"))
    price_filter = post.get("price").split(";")
    min_price_filter = int(price_filter[0])
    max_price_filter = int(price_filter[1])
    if post.get("stock") == "on":
        return ProductInShop.objects.filter(quantity__gt=0)
    if post.get("name_product"):
        return ProductInShop.objects.filter(product__name=post.get("name_product"))
    return ProductInShop.objects.filter(
        price__gte=min_price_filter, price__lte=max_price_filter
    )


def get_maxprice(pid: list, maxprice=0) -> ProductInShop:

    for product in pid:
        if product.price > maxprice:
            maxprice = product.price
    return maxprice


def paginator(obj, request):
    paginator_catalog = Paginator(obj, 4)
    page_number = request.get("page_catalog")
    if page_number is None:
        page_number = 1
    catalog_page_obj = paginator_catalog.get_page(page_number)
    return catalog_page_obj
