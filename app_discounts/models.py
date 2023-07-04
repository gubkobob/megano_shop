from django.db import models
from app_catalog.models import ProductInShop, Product
from django.utils.translation import gettext_lazy as _


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



    # Если у продукта есть цена, но нет цены со скидкой, но есть скидка то

    # Отдельные
    # - получить все скидки на указанный список товаров или на один товар;
    # - получить приоритетную скидку на указанный список товаров или на один товар;
    # - получить скидку на корзину;
    # - рассчитать цену со скидкой на товар с дополнительным необязательным параметром ― цена товара.


    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return str(self.product)


class DiscountPrice(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, verbose_name='скидка',
                                related_name='discount_price')
    percent = models.IntegerField(blank=True, null=True, verbose_name=_('процентная скидка'))
    quantity = models.IntegerField(blank=True, null=True, verbose_name=_('количественная скидка'))

    def get_price_product(self):
        if self.discount.type_discount == 'процент':
            return self.discount.product.price * (int(self.percent * 0.10))

        elif self.discount.type_discount == 'количество':
            return self.discount.product.price - self.quantity

    class Meta:
        verbose_name = 'Значение скидки'
        verbose_name_plural = 'Значения скидок'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super(DiscountPrice, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

        if self.discount.type_discount == 'процент':
            self.quantity = 0
            if self.percent > 30:
                self.percent = 30

        elif self.discount.type_discount == 'количество':
            self.percent = 0
            if self.quantity >= self.discount.product.price:
                self.quantity = self.discount.product.price // 20

        elif self.discount.type_discount == 'процент и количество':

            if self.percent > 30:
                self.percent = 10

            if self.quantity >= self.discount.product.price:
                self.quantity = self.discount.product.price // 40

        return super(DiscountPrice, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return str(self.discount)
