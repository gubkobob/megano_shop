from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class SettingsModel(models.Model):
    limited_edition_products = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(16)],
                                                   null=True, blank=True, verbose_name='Товары ограниченного тиража')
    hot_offers = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)],
                                     null=True, blank=True, verbose_name='Горячие предложения')
    popular_products = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)],
                                           null=True, blank=True, verbose_name='Популярные товары')
    products_banner = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)],
                                       null=True, blank=True, verbose_name='Баннеры на главной')
    viewed_products = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],
                                          null=True, blank=True, verbose_name='Просмотренные товары')
    selected_categories = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)],
                                              null=True, blank=True, verbose_name='Избранные категории')
    cache_time = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(86400)],
                                     null=True, blank=True, verbose_name='Время обновления кэша')

    def get_absolute_url(self):
        return '/settings'

