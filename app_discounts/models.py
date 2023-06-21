from django.db import models
from app_catalog.models import ProductInShop, Product
from django.utils.translation import gettext_lazy as _


class Discount(models.Model):
    product = models.ForeignKey(ProductInShop, on_delete=models.CASCADE, verbose_name='Продукт',
                                related_name='product_discount')
    # price_product = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name=_('Цена продукта'))
    discount = models.IntegerField(default=0, verbose_name=_('Скидка'))
    # Если у продукта есть цена, но нет цены со скидкой, но есть скидка то
    start_discount = models.DateTimeField()
    end_discount = models.DateTimeField()

    # Отдельные
    # - получить все скидки на указанный список товаров или на один товар;
    # - получить приоритетную скидку на указанный список товаров или на один товар;
    # - получить скидку на корзину;
    # - рассчитать цену со скидкой на товар с дополнительным необязательным параметром ― цена товара.

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    # def save(
    #     self, force_insert=False, force_update=False, using=None, update_fields=None
    # ):
    #     super(Discount, self).save(
    #         force_insert=False, force_update=False, using=None, update_fields=None
    #     )
    #     if self.price_discount <= 0 and (self.discount > 0):
    #         self.price_discount = (self.price_product // self.discount)
    #         return super(Discount, self).save(force_insert, force_update, using, update_fields)
    #     return


class DiscountList(models.Model):
    pass


class DiscountPrior(models.Model):
    pass


class DiscountCart(models.Model):
    pass


class DiscountPrice(models.Model):
    pass
