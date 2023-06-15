from django.http import JsonResponse
from config import settings
from app_catalog.models import Product
from django.core import serializers

class CartServicesMixin:
    """
    Класс - примесь для использования сервисов для работы с корзиной товаров
    """

    def add_product_to_cart(self, pk:int):
        """
        функция добавления товара в корзину
        """
        product = Product.objects.get(id=pk)
        print(f'{product.name} добавлен в корзину')

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

    def add_to_in_comparison(self, product_id):
        """
        Добавить продукт в сравнение.
        """
        product = Product.objects.get(id=product_id)
        subspecification_dict = {}
        specification_dict = {}

        print(product.specification.all().values())
        print('OPEN', (x for x in product.specification.all().values()))
        for subspecification in product.specification.select_related('product').all():
            print(subspecification.name_specification)
            subspecification_dict['subspecification'] = subspecification.name_specification
            print(subspecification_dict)
            for dubsub in subspecification.subspecification.get_queryset().values('name_subspecification', 'text_subspecification'):
                subspecification_dict[str(subspecification.name_specification)] = dubsub
                # print(test)
            # print('OER', subspecification.subspecification.get_queryset().values('name_subspecification', 'text_subspecification'))
            # print('tt', subspecification.subspecification.values('name_subspecification', 'text_subspecification'))
            # subspecification_dict['subspecification'] = subspecification.subspecification.values_list('name_subspecification', 'text_subspecification')

        print('subspecification_dict', subspecification_dict)
        for exsubspecification in subspecification_dict.values():
            print('TTTT', exsubspecification)
            # print('ttt', subspecification_dict[exsubspecification])
            specification_dict['specification'] = {'subspecification': exsubspecification}
        print(specification_dict.values())
        print(specification_dict)

        # print(specification)
        # for spec in product.specification.select_related('product'):
        #     subspecification = spec.subspecification.values('name_subspecification', 'text_subspecification')
        #     print(subspecification)
        #     serialized_data = serializers.serialize("json", subspecification)
        #     specification['specification'] = {str(spec): serialized_data}

        # specification = list(product.specification.get().subspecification.values('name_subspecification', 'text_subspecification'))

        if product not in self.comparison:
            self.comparison[product_id] = {
                'product_id': product.id,
                'product_name': product.name,
                'product_price': int(product.price),
                'product_image': str(product.image.url) if product.image else '',
                'specification': self.comparison,
                'specifications': specification_dict,

            }
        # print(self.comparison)
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
        return list(self.comparison[item[1]] for item in enumerate(self.comparison) if item[0] < quantity)

    def get_len_goods_to_in_comparison(self):

        """
        Получение количества товаров в сравнении.
        """
        return len(self.comparison.keys())



#