
"""
Сервисы для работы с корзиной товаров
"""

class CartServicesMixin:
    """
    Класс - примесь для использования сервисов для работы с корзиной товаров
    """

    def add_product_to_cart(self):
        """
        функция добавления товара в корзину
        """

    def remove_product_from_cart(self):
        """
        функция удаления товара из корзины
        """

    def change_num_of_product_in_cart(self):
        """
        функция изменения количества товара в корзине
        """

    def get_products_list_from_cart(self):
        """
        функция получения списка товаров в корзине
        """

    def get_num_of_products_in_cart(self):
        """
        функция получения количества товаров в корзине
        """