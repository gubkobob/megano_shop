from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from app_cart.models import CartRegisteredUser
from app_catalog.models import ProductInShop


User = get_user_model()


class Order(models.Model):
    """
    Модель заказа
    """

    STATUS_ORDER_CHOICES = [
        ('not paid', 'Не оплачен'),
        ('paid for', 'Оплачен')
    ]

    DELIVERY_METHOD_CHOICES = [
        ('ordinary', 'Обычная доставка'),
        ('express', 'Экспресс доставка')
    ]

    PAYMENT_METHOD_CHOICES = [
        ('online', 'Онлайн картой'),
        ('someone', 'Онлайн со случайного чужого счета')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Пользователь"), related_name='orders')
    full_name = models.CharField(max_length=255, verbose_name=_("Фамилия Имя Отчество"))
    phone_number = models.CharField(max_length=20, blank=True,
                                    help_text=_("Contact phone number"), verbose_name=_("Телефон"))
    email = models.EmailField(max_length=50, verbose_name=_("E-mail"))
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Город"))
    address = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_("Адрес доставки"))
    delivery = models.CharField(max_length=100, choices=DELIVERY_METHOD_CHOICES,
                                default=_('ordinary'), verbose_name=_("Способ доставки"))
    payment = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES,
                               default=_('online'), verbose_name=_("Способ Оплаты"))
    comment = models.TextField(null=True, blank=True, verbose_name=_("Комментарий к заказу"))
    created_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата создания заказа"))
    status = models.CharField(max_length=25, choices=STATUS_ORDER_CHOICES, default=_('not paid'),
                              verbose_name=_("Статус заказа"))

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
