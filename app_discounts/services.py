"""
Сервисы для работы со скидками
"""
from app_catalog.models import ProductInShop, Product
from .models import Discount
from django.db.models.functions import TruncMonth, TruncDay
from django.db.models import Count


class DiscountsServicesMixin:
    """
    Класс - примесь для использования сервисов для работы со скидками
    """


    def get_discounts_page(self):
        """
        функция получения страницы со скидками
        """
        discount = Discount

        context = {}
        category_is = []
        content = []

        for t in discount.objects.values():
            print(Product.objects.get(products_in_shop=t['product_id']))
            context[t['id']] = {
                'datetime_start': discount.objects.get(product=t['product_id']).start_discount,
                'datetime_end': discount.objects.get(product=t['product_id']).end_discount,
                'category_product': Product.objects.get(products_in_shop=t['product_id']).category,
                'product_name': Product.objects.get(products_in_shop=t['product_id']),
            }
            category_is.append(Product.objects.get(products_in_shop=t['product_id']).category)


        # for context_ in context.values():
        #     for content_ in context_:
        #         print(context_[content_])
        #         content.append(context_)

        return list(_context_ for _context_ in context.values())

    def get_discounts(self):
        """
        функция получения скидок на товары
        """

    def get_total_discount(self):
        """
        метод получения скидок на указанный список товаров или на один товар
        """
        pass

    def get_priority_discount(self):
        """
        метод получения приоритетной скидки на указанный список товаров или на один товар
        """
        pass

    def post_price_discount(self):
        """
        метод рассчета цены со скидкой на товар с дополнительным необязательным параметром «Цена товара»
        """
        pass