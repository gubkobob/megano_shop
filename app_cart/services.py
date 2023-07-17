from app_catalog.models import ProductInShop
from config import settings


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

    def add_to_in_comparison(self, product_id):
        """
        Добавить продукт в сравнение.
        """

        product = ProductInShop.objects.get(id=product_id)

        if product not in self.comparison:
            self.comparison[product_id] = {
                "product_id": product_id,
                "product_name": product.product.name,
                "product_price": int(product.price),
                "product_image": str(product.product.image_main.url)
                if product.product.image_main
                else "",
                "specification": list(
                    product.product.specification.get().subspecification.values(
                        "name_subspecification", "text_subspecification"
                    )
                )
                if product.product.specification
                else "",
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

    def remove_from_comparison(self, product_id):
        """
        Удаление товара из сравнения.
        """
        self.comparison.pop(product_id)
        self.save_to_in_comparison()

    def get_goods_to_in_comparison(self, quantity=3):
        """
        Получения товаров в сравнении.
        """
        return list(
            self.comparison[item[1]]
            for item in enumerate(self.comparison)
            if item[0] < quantity
        )

    def get_len_goods_to_in_comparison(self):

        """
        Получение количества товаров в сравнении.
        """
        return len(self.comparison.keys())
