"""
Сервисы для работы со скидками
"""
from .models import Discount


class DiscountsServicesMixin:
    """
    Класс - примесь для использования сервисов для работы со скидками
    """

    def get_discounts_page(self):
        """
        функция получения страницы со скидками
        """
        # Запуск проверки на соотвествие скидки по времени
        for _ in Discount.objects.values():
            Discount.objects.get(id=_['id']).available_monitoring()
        return

    def get_discounts(self, product_id):
        """
        функция получения скидок на товары
        """
        Discount.get_price_product(self=product_id)

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
