"""
Сервисы для работы с каталогом, товарами, магазинами
"""


class ProductServicesMixin:
    """
    Класс - примесь для использования сервисов для работы с товарами
    """

    def add_review_to_product(self):
        """
        функция добавления отзыва к товару
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


