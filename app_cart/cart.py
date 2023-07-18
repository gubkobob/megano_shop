from copy import deepcopy
from decimal import Decimal

from app_catalog.models import ProductInShop
from app_discounts.models import Coupon, Discount
from django.conf import settings

from .models import CartRegisteredUser


class Cart(object):
    """
    Класс для корзины незарегистрированного пользователя
    """

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

        # сохранение текущего примененного купона
        self.coupon_id = self.session.get("coupon_id")

    def add(self, product_in_shop, quantity=1, update_quantity=False):
        """
        Добавить обьект склада в корзину или обновить его количество.
        """

        product_in_shop_id = str(product_in_shop.id)
        if product_in_shop_id not in self.cart:
            self.cart[product_in_shop_id] = {
                "quantity": 0,
                "price": str(product_in_shop.price),
                "price_discount": float(
                    Discount.objects.get(
                        product_id=product_in_shop.id
                    ).get_price_product()
                )
                if Discount.objects.filter(product_id=product_in_shop.id).exists()
                else 0,
            }
        if update_quantity:
            if quantity <= product_in_shop.quantity:
                self.cart[product_in_shop_id]["quantity"] = quantity
            else:
                self.cart[product_in_shop_id]["quantity"] = product_in_shop.quantity
        else:
            if (
                self.cart[product_in_shop_id]["quantity"] + quantity
            ) <= product_in_shop.quantity:
                self.cart[product_in_shop_id]["quantity"] += quantity
            else:
                self.cart[product_in_shop_id]["quantity"] = product_in_shop.quantity
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
        # копия для того, чтобы не изменялся обьект корзины, т.к. обьекты типа ProductInShop в сессиях django хранить нельзя
        cart_copy = deepcopy(self.cart)
        for idx, item in cart_copy.items():
            item["product_in_shop"] = ProductInShop.objects.filter(id=idx).first()
            yield item

    def __len__(self):
        """
        Подсчет всех обьектов склада в корзине.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости обьектов склада в корзине.
        """
        return sum(
            Decimal(item["price_discount"]) * item["quantity"]
            if item["price_discount"]
            else Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def clear(self):
        """
        удаление корзины из сессии.
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    @property
    def coupon(self):
        """Функция промокода"""
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        """Функция получения скидки по промокоду"""
        if self.coupon:
            return (self.coupon.discount / Decimal("100")) * self.get_total_price()
        return Decimal("0")

    def get_total_price_after_discount(self):
        """Функция получения итоговой суммы со скидкой"""
        return self.get_total_price() - self.get_discount()


class CartDB(object):
    """
    Класс для корзины зарегистрированного пользователя
    """

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        self.user = request.user
        cart = CartRegisteredUser.objects.filter(user_id=self.user.id).all()
        self.cart = cart

        # сохранение текущего примененного купона
        self.coupon_id = self.session.get("coupon_id")

    def add(self, product_in_shop, quantity=1, update_quantity=False):
        """
        Добавить обьект склада в корзину или обновить его количество.
        """
        product = self.cart.filter(product_in_shop_id=product_in_shop.id).first()
        if not product:
            product = CartRegisteredUser(
                user_id=self.user.id,
                product_in_shop_id=product_in_shop.id,
                quantity=0,
                price=product_in_shop.price,
                price_discount=Discount.objects.get(
                    product_id=product_in_shop.id
                ).get_price_product()
                if Discount.objects.filter(product_id=product_in_shop.id).exists()
                else "0",
            )
        if update_quantity:
            if quantity <= product_in_shop.quantity:
                product.quantity = quantity
            else:
                product.quantity = product_in_shop.quantity
        else:
            if (product.quantity + quantity) <= product_in_shop.quantity:
                product.quantity += quantity
            else:
                product.quantity = product_in_shop.quantity
        product.save()

    def save(self):
        for product in self.cart:
            product.save()

    def remove(self, product_in_shop):
        """
        Удаление обьект склада из корзины.
        """
        self.cart.filter(product_in_shop_id=product_in_shop.id).delete()

    def __iter__(self):
        """
        Перебор элементов в корзине.
        """
        for item in self.cart:
            yield item

    def __len__(self):
        """
        Подсчет всех обьектов склада в корзине.
        """
        count = 0
        for product in self.cart:
            count += product.quantity
        return count

    def get_total_price(self):
        """
        Подсчет стоимости обьектов склада в корзине.
        """
        total_price = 0
        for product in self.cart:
            if product.price_discount:
                total_price += product.price_discount * product.quantity
            else:
                total_price += product.price * product.quantity
        return total_price

    @property
    def coupon(self):
        """Функция промокода"""
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        """Функция получения скидки по промокоду"""
        if self.coupon:
            return (self.coupon.discount / Decimal("100")) * self.get_total_price()
        return Decimal("0")

    def get_total_price_after_discount(self):
        """Функция получения итоговой суммы со скидкой"""
        return round(self.get_total_price() - self.get_discount(), 2)


def change_products_in_cart_db_from_cart(cart_db: CartDB, cart: Cart):
    """
    Функция добавление товаров из корзины незарегистрированного пользователя в корзину БД при аутентификации
    """
    for product in cart:
        cart_db.add(
            product_in_shop=product["product_in_shop"],
            quantity=product["quantity"],
            update_quantity=False,
        )
    cart_db.save()
