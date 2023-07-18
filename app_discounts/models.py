from app_catalog.models import Product, ProductInShop
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Discount(models.Model):
    """Модель Скидок"""

    types = [
        (_("процент"), "процент"),
        (_("количество"), "количество"),
        (_("процент и количество"), "процент и количество"),
    ]

    product = models.ForeignKey(
        ProductInShop,
        on_delete=models.CASCADE,
        verbose_name="Продукт",
        related_name="product_discount",
    )
    type_discount = models.CharField(
        choices=types,
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("тип скидки"),
    )

    start_discount = models.DateTimeField()
    end_discount = models.DateTimeField()

    user_created = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь создавший скидку"),
        blank=User,
        null=True,
        auto_created=User,
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания скидки"
    )
    available = models.BooleanField(default=True, verbose_name="Доступность скидки")

    percent = models.IntegerField(
        blank=True, null=True, verbose_name=_("процентная скидка")
    )
    quantity = models.IntegerField(
        blank=True, null=True, verbose_name=_("количественная скидка")
    )

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def get_price_product(self):
        """Функция получения цены продукта с учетом скидки"""
        if self.type_discount == "процент":
            return round(
                float(self.product.price)
                - (float(self.product.price) * (self.percent / 100)),
                2,
            )

        elif self.type_discount == "количество":
            return round(self.product.price - self.quantity, 2)

        elif self.type_discount == "процент и количество":
            return round(
                (
                    float(self.product.price)
                    - (float(self.product.price) * (self.percent / 100))
                )
                - self.quantity,
                2,
            )

    def available_monitoring(self):
        """Функция проверки конца скидки по сегоднешней дате"""
        if self.end_discount.date() < timezone.now().date():
            self.available = False
            self.save()
        else:
            self.available = True
            self.save()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """Функция сохранения """
        super(Discount, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

        if self.type_discount == "процент":
            self.quantity = 0
            if self.percent > 30:
                self.percent = 30

        elif self.type_discount == "количество":
            self.percent = 0
            if self.quantity >= self.product.price:
                self.quantity = round(self.product.price / 20, 2)

        elif self.type_discount == "процент и количество":

            if self.percent > 30:
                self.percent = 10

            if self.quantity >= self.product.price:
                self.quantity = round(self.product.price / 40, 2)

        return super(Discount, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return str(self.product)


class Coupon(models.Model):
    """Модель Промокода"""
    code = models.CharField(max_length=50, unique=True, verbose_name="Промокод")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    active = models.BooleanField()

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def __str__(self):
        return self.code
