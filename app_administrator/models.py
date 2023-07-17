from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class SettingsModel(models.Model):
    limited_edition_products = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(16)],
        null=True,
        blank=True,
        verbose_name="Товары ограниченного тиража",
    )
    hot_offers = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9)],
        null=True,
        blank=True,
        verbose_name="Горячие предложения",
    )
    popular_products = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        null=True,
        blank=True,
        verbose_name="Популярные товары",
    )
    products_banner = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        null=True,
        blank=True,
        verbose_name="Баннеры на главной",
    )
    count_viewed = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        null=True,
        blank=True,
        verbose_name="История просмотра",
    )
    selected_categories = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        null=True,
        blank=True,
        verbose_name="Избранные категории",
    )
    cache_time = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(86400)],
        null=True,
        blank=True,
        verbose_name="Время обновления кэша",
    )
    price_express_delivery = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        null=True,
        blank=True,
        verbose_name="Стоимость экспресс доставки",
    )
    price_ordinary_delivery = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(400)],
        null=True,
        blank=True,
        verbose_name="Стоимость обычной доставки",
    )
    min_total_price_order = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4000)],
        null=True,
        blank=True,
        verbose_name="Минимальная сумма заказа",
    )

    class Meta:
        verbose_name = "Настройки и сброс всего кэша"
        verbose_name_plural = "Административные настройки"
