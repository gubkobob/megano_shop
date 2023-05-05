"""
Сервисы для работы с каталогом, товарами, магазинами
"""
from .models import Comments

class ProductServicesMixin:

    def add_review_to_product(self):
        """
        функция добавления отзыва к товару
        """
        if self.request.method == 'POST':
            comments = Comments.objects.get_or_create(comments=self.request.POST['comments'])
            comments.save()
            return

    def get_viewed_products_history(self):
        """
        функция получения списка просмотренных товаров
        """

    def add_viewed_products_history(self):
        """
        функция добавления товара к списку просмотренных
        """

    def get_list_comments_on_products(self) -> list[str]:
        """
        функция получения списка комментариев к продукту
        """
        if self.request.method == 'GET':
            comments = Comments.objects.get(goods=self.request.GET['goods'])
            return list(comments.objects.get(comments))

    def get_discount_on_products(self):
        """
        функция получения скидки к продукту
        """

    def get_quantity_comments_on_products(self) -> int:
        """
        функция получения количество комментариев к продукту
        """
        if self.request.method == 'GET':
            comments = Comments.objects.get(goods=self.request.GET['goods'])
            return len(comments.objects.get(comments))


class ShopServicesMixin:
    """
    Класс - примесь для использования сервисов для работы с магазинами
    """

