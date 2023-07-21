from app_catalog.models import ProductInShop
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CartRegisteredUser(models.Model):
    """Модель корзины зарегисирированных пользователей"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Пользователь")
    )
    product_in_shop = models.ForeignKey(
        ProductInShop, on_delete=models.CASCADE, verbose_name=_("Товары")
    )
    quantity = models.PositiveIntegerField(
        default=0, verbose_name=_("Количество товара")
    )
    price = models.DecimalField(
        default=0, max_digits=10, decimal_places=2, verbose_name="Цена товара"
    )
    price_discount = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Цена товара со скидкой",
    )

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
