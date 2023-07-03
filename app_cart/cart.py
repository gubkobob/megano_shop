from decimal import Decimal
from django.conf import settings
from app_catalog.models import ProductInShop


class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product_in_shop, quantity=1, update_quantity=False):
        """
        Добавить обьект склада в корзину или обновить его количество.
        """
        product_in_shop_id = str(product_in_shop.id)
        if product_in_shop_id not in self.cart:
            self.cart[product_in_shop_id] = {'quantity': 0,
                                     'price': str(product_in_shop.price)}
        if update_quantity:
            self.cart[product_in_shop_id]['quantity'] = quantity
        else:
            self.cart[product_in_shop_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product_in_shop):
        """
        Удаление обьект склада из корзины.
        """
        product_in_shop_id = str(product_in_shop.id)
        if product_in_shop_id in self.cart:
            del self.cart[product_in_shop_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение обьекта склада из базы данных.
        """
        product_in_shop_ids = self.cart.keys()
        # получение объектов product_in_shop и добавление их в корзину
        products_in_shops = ProductInShop.objects.filter(id__in=product_in_shop_ids)
        for product_in_shop in products_in_shops:
            self.cart[str(product_in_shop.id)]['product_in_shop'] = product_in_shop

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех обьектов склада в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости обьектов склада в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
