from django.shortcuts import render

from app_cart.services import ComparisonServicesMixin


def add_in_comparison(request, product):
    """
    Функция добавляет в список сравнений продукт
    """
    comparison = ComparisonServicesMixin(request=request)
    comparison.add_to_in_comparison(product=product)


def list_product_in_comparison(request):
    comparison = ComparisonServicesMixin(request=request)
    content = comparison.get_goods_to_in_comparison()
    return render(request, 'shops/comparison.jinja2', {'content': content})
