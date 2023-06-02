from django.db import models
from app_catalog.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='имя заказчика')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='заказчик')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='количество')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
