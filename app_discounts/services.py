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

        context = {}

        # Запуск проверки на соотвествие скидки по времени
        for _ in Discount.objects.values():
            Discount.objects.get(id=_["id"]).available_monitoring()

        # Сбор данных для отправки в шаблон
        for product in (
            Discount.objects.get_queryset()
            .filter(available=True)
            .select_related("product")
            .order_by("start_discount")
        ):
            context[product.id] = {
                "product_id": product.product.id,
                "datetime_start": product.start_discount,
                "datetime_end": product.end_discount,
                "category_product": product.product.product.category,
                "product_name": product.product.product.name,
                "product_price": product.product.price,
                "product_discount_price": product.get_price_product(),
                "product_type_discount": product.type_discount,
                "product_image": str(product.product.product.image_main.url)
                if product.product.product.image_main
                else "",
            }

        return list(_context_ for _context_ in context.values())

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
