from config import settings


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


class ComparisonServicesMixin:
    """
    Класс - примесь для использования сервисов для работы с сравнение товаров
    """
    def __init__(self, request):
        """
        Инициализируем список сравнений.
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
        product_id = str(product.id)
        if product_id not in self.comparison:
            self.comparison[product_id] = {
                'product_id': product.id,
                'product_name': product.name,
                'product_price': int(product.price),
            }
        self.save_to_in_comparison()

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
        product_id = str(product.id)
        if product_id in self.comparison:
            del self.comparison[product_id]
            self.save_to_in_comparison()

    def get_goods_to_in_comparison(self, quantity=3):
        """
        Получения товаров в сравнении.
        """

        return list(self.comparison[item[1]] for item in enumerate(self.comparison) if item[0] < quantity)

    def get_len_goods_to_in_comparison(self):

        """
        Получение количества товаров в сравнении.
        """
        return len(self.comparison[item] for item in self.comparison)
