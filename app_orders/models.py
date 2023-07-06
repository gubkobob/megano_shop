from django.contrib.auth import get_user_model
from django.db import models

from app_cart.models import CartRegisteredUser
from app_catalog.models import ProductInShop


User = get_user_model()

class Order(models.Model):
    """
    Модель заказа
    """
    DELIVERY_TYPE_ORDINARY = 'ordinary'
    DELIVERY_TYPE_EXPRESS = 'express'

    PAYMENT_METHOD_ONLINE = 'online'
    PAYMENT_METHOD_SOMEONE = 'someone'

    STATUS_NOT_PAID = 'not paid'
    STATUS_PAID_FOR = 'paid for'

    STATUS_ORDER_CHOICES = [
        (STATUS_NOT_PAID, 'Не оплачен'),
        (STATUS_PAID_FOR, 'Оплачен')

    ]

    DELIVERY_METHOD_CHOICES = [
        (DELIVERY_TYPE_ORDINARY, 'Обычная доставка'),
        (DELIVERY_TYPE_EXPRESS, 'Экспресс доставка')
    ]

    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_METHOD_ONLINE, 'Онлайн картой'),
        (PAYMENT_METHOD_SOMEONE, 'Онлайн со случайного чужого счета')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name='orders')
    full_name = models.CharField(max_length=255, verbose_name="Фамилия Имя Отчество")
    phone_number = models.CharField(max_length=20, blank=True,
                                    help_text="Contact phone number", verbose_name="Телефон")
    email = models.EmailField(max_length=50, verbose_name="E-mail")
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Город")
    address = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Адрес доставки")
    delivery = models.CharField(max_length=100, choices=DELIVERY_METHOD_CHOICES,
                                   default=DELIVERY_TYPE_ORDINARY, verbose_name="Способ доставки")
    payment = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES,
                               default=PAYMENT_METHOD_ONLINE, verbose_name="Способ Оплаты")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий к заказу")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата создания заказа")
    status = models.CharField(max_length=25, choices=STATUS_ORDER_CHOICES, default=STATUS_NOT_PAID,
                              verbose_name="Статус заказа")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    """
    Модель товаров в заказе
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    product_in_shop = models.ForeignKey(ProductInShop, on_delete=models.CASCADE, verbose_name='Товар',
                                        related_name='order_items')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество товара')
    price = models.DecimalField(default=1, max_digits=10, decimal_places=2, verbose_name='Цена товара')

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
