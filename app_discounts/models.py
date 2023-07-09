from django.contrib.auth import get_user_model
from django.db import models
from app_catalog.models import ProductInShop, Product
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Discount(models.Model):

    types = [
        ('процент', 'процент'),
        ('количество', 'количество'),
        ('процент и количество', 'процент и количество'),
    ]

    product = models.ForeignKey(ProductInShop, on_delete=models.CASCADE, verbose_name='Продукт',
                                related_name='product_discount')
    type_discount = models.CharField(choices=types, max_length=20,
                                   blank=True, null=True, verbose_name=_('тип скидки'))

    start_discount = models.DateTimeField()
    end_discount = models.DateTimeField()

    user_created = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь создавший скидку'),
                                     blank=User, null=True, auto_created=User)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания скидки')
    available = models.BooleanField(default=True, verbose_name='Доступность скидки')

    percent = models.IntegerField(blank=True, null=True, verbose_name=_('процентная скидка'))
    quantity = models.IntegerField(blank=True, null=True, verbose_name=_('количественная скидка'))

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def get_price_product(self):
        if self.type_discount == 'процент':
            return float(self.product.price) - (float(self.product.price) * (self.percent / 100))

        elif self.type_discount == 'количество':
            return self.product.price - self.quantity

        elif self.type_discount == 'процент и количество':
            return (float(self.product.price) - (float(self.product.price) * (self.percent / 100))) - self.quantity

    # Отдельные
    # - получить все скидки на указанный список товаров или на один товар;
    # - получить приоритетную скидку на указанный список товаров или на один товар;
    # - получить скидку на корзину;
    # - рассчитать цену со скидкой на товар с дополнительным необязательным параметром ― цена товара.

    def available_monitoring(self):
        if self.end_discount.date() < timezone.now().date():
            self.available = False
            self.save()
        else:
            self.available = True
            self.save()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super(Discount, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

        if self.type_discount == 'процент':
            self.quantity = 0
            if self.percent > 30:
                self.percent = 30

        elif self.type_discount == 'количество':
            self.percent = 0
            if self.quantity >= self.product.price:
                self.quantity = self.product.price // 20

        elif self.type_discount == 'процент и количество':

            if self.percent > 30:
                self.percent = 10

            if self.quantity >= self.product.price:
                self.quantity = self.product.price // 40

        return super(Discount, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return str(self.product)


# class Coupon(models.Model):
#     code = models.CharField(max_length=50, unique=True)
#     valid_from = models.DateTimeField()
#     valid_to = models.DateTimeField()
#     discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
#     active = models.BooleanField()
#
# class DiscountPrice(models.Model):
#     discount = models.ForeignKey(Discount, on_delete=models.CASCADE, verbose_name='скидка',
#                                 related_name='discount_price')
#     percent = models.IntegerField(blank=True, null=True, verbose_name=_('процентная скидка'))
#     quantity = models.IntegerField(blank=True, null=True, verbose_name=_('количественная скидка'))
#
#     def get_price_product(self):
#         if self.discount.type_discount == 'процент':
#             return float(self.discount.product.price) - (float(self.discount.product.price) * ((self.percent) / 100))
#
#         elif self.discount.type_discount == 'количество':
#             return self.discount.product.price - self.quantity
#
#         elif self.discount.type_discount == 'процент и количество':
#             return (float(self.discount.product.price) - (float(self.discount.product.price) * ((self.percent) / 100))) - self.quantity
#
#     def get_percent(self):
#         return self.percent
#
#     def get_quantity(self):
#         return self.percent
#
#     class Meta:
#         verbose_name = 'Значение скидки'
#         verbose_name_plural = 'Значения скидок'
#
#     def save(
#         self, force_insert=False, force_update=False, using=None, update_fields=None
#     ):
#         super(DiscountPrice, self).save(
#             force_insert=False, force_update=False, using=None, update_fields=None
#         )
#
#         if self.discount.type_discount == 'процент':
#             self.quantity = 0
#             if self.percent > 30:
#                 self.percent = 30
#
#         elif self.discount.type_discount == 'количество':
#             self.percent = 0
#             if self.quantity >= self.discount.product.price:
#                 self.quantity = self.discount.product.price // 20
#
#         elif self.discount.type_discount == 'процент и количество':
#
#             if self.percent > 30:
#                 self.percent = 10
#
#             if self.quantity >= self.discount.product.price:
#                 self.quantity = self.discount.product.price // 40
#
#         return super(DiscountPrice, self).save(force_insert, force_update, using, update_fields)
#
#
#     def __str__(self):
#         return str(self.discount)
