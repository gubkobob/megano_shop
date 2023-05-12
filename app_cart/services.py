
"""
Сервисы для работы с корзиной товаров
"""
from config import settings


class CartServicesMixin:
    """
    Класс - примесь для использования сервисов для работы с корзиной товаров
    """

    def add_product_to_cart(self):
        """
        функция добавления товара в корзину
        """


class ComparisonServicesMixin:
    """
    Класс - примесь для использования сервисов для работы с сравнение товаров
    """
    def __init__(self, request):
        """
        Инициализируем список сравнений
        """
        self.session = request.session
        comparison = self.session.get(settings.COMPARISON_SESSION_ID)
        if not comparison:
            comparison = self.session[settings.COMPARISON_SESSION_ID] = {}
        self.comparison = comparison

    def add_to_in_comparison(self, product):
        """
        Добавить продукт в сравнение.
        """

    def save_to_in_comparison(self):
        """
        Сохрание сравнения
        """

        # Обновление сессии comparison
        self.session[settings.COMPARISON_SESSION_ID] = self.comparison
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove_from_comparison(self, product):
        """
        Удаление товара из сравнения.
        """

    def get_goods_to_in_comparison(self):
        """
        Получения товаров в сравнении.
        """

    def get_len_goods_to_in_comparison(self):

        """
        Получение количества товаров в сравнении.
        """
