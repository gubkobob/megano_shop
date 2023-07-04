"""
Сервисы для работы со скидками
"""
import datetime
from django.utils import timezone
from app_catalog.models import ProductInShop, Product
from .models import Discount, DiscountPrice



class DiscountsServicesMixin:
    """
    Класс - примесь для использования сервисов для работы со скидками
    """


    def get_discounts_page(self):
        """
        функция получения страницы со скидками
        """
        context = {}

        # - /СДЕЛАНО/ - фильтр добавить

        # - //Добавить айдишник// + //поправить шаблон на переход по айдишнику//
        # - //Добавить картинки//
        # - //Добавить цену со скидкой и без + вывод какая скидка.//
        # - ПРИОРИТЕТ - Начать логику корзины + добавить логику цены со скидкой через *ЕСЛИ* / Совместить с 3 пунктом



        # Вопрос правильности фильтра



        #
        for t in Discount.objects.filter(end_discount__day=timezone.now().day + 1).values():
            context[t['id']] = {
                'product_id': Discount.objects.get(product=t['product_id']).product_id,
                'datetime_start': Discount.objects.get(product=t['product_id'], start_discount=t['start_discount']).start_discount,
                'datetime_end': Discount.objects.get(product=t['product_id'], end_discount=t['end_discount']).end_discount,
                'category_product': Product.objects.get(products_in_shop=t['product_id']).category,
                'product_name': Product.objects.get(products_in_shop=t['product_id']),
                'product_price': ProductInShop.objects.get(id=t['product_id']).price,
                'product_discount_price':
                    DiscountPrice.objects.get(discount=t['id']).get_price_product(),
                'product_type_discount': Discount.objects.get(product=t['product_id']).type_discount,
                'product_image': str(Product.objects.get(products_in_shop=t['product_id']).image_main.url)
                if Product.objects.get(products_in_shop=t['product_id']).image_main else ''
            }

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