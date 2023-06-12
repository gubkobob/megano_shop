from django.shortcuts import render, redirect
from django.contrib import messages
from app_cart.services import ComparisonServicesMixin


def add_in_comparison(request, product_id):
    """
    Функция добавляет в список сравнений продукт и возвращает обратно на страницу
    """
    comparison = ComparisonServicesMixin(request=request)
    comparison.add_to_in_comparison(product_id=product_id)
    # messages.add_message(request, messages.INFO, 'Товар добавлен в сравнение')
    # print(messages)
    return redirect('appcatalog:categories_list')


def list_product_in_comparison(request):
    """
    Функция выводит список продуктов в списке сравнения
    """
    comparison = ComparisonServicesMixin(request=request)
    content = comparison.get_goods_to_in_comparison()
    count_goods = comparison.get_len_goods_to_in_comparison()
    return render(request, 'shops/comparison.jinja2', {'content': content,
                                                       'count_goods': count_goods})


def remove_product_in_comparison(request, product_id):
    """
    Функция удаляет товар из списка сравнения и возвращает обратно в список сравнений
    """
    comparison = ComparisonServicesMixin(request=request)
    comparison.remove_from_comparison(product_id=product_id)
    return redirect('app_cart:comparison_list')

#   для дебага нужно было, можно удалять
# def get_len_goods_to_in_comparison(request):
#     comparison = ComparisonServicesMixin(request=request)
#     x = comparison.get_len_goods_to_in_comparison()
#     return x
