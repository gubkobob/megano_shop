from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Categories(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile', verbose_name=_('Профиль'))
    goods = models.CharField(on_delete=models.CASCADE, verbose_name=_('Товары'))
    comments = models.TextField(on_delete=models.CASCADE, verbose_name=_('Комментарии'))


def product_image_directory_path(instance: 'Products', filename: str) -> str:
    """Фукнция директории изображения продукта
    возвращает айди продукта и имя файла
    """
    return 'products/product_{pk}/image/{filename}'.format(
        pk=instance.pk,
        filename=filename
    )


class Products(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Имя'))
    image = models.FileField(null=True, blank=True, upload_to=product_image_directory_path, verbose_name=_('Фото'))
    descriptions = models.TextField(null=False, blank=True, verbose_name=_('Описание'))
    categories = models.ManyToManyField(Categories, on_delete=models.CASCADE, related_name='categories', verbose_name=_('Категория'))
    limited_edition = models.CharField(max_length=255, verbose_name=_('Ограниченный выпуск'))
    price = models.FloatField(default=0, verbose_name=_('Цена'))
    numbers_sellers = models.CharField(default=0, max_length=255, verbose_name=_('Количество продавцов'))
    manufacturer = models.CharField(default=0, max_length=255, verbose_name=_('Производитель'))
    many_product = models.FloatField(default=0, max_length=255, verbose_name=_('Количество товара'))
    discount = models.SmallIntegerField(default=0, verbose_name=_('Скидка'))


class Comments(models.Model):
    goods = models.ManyToManyField(Products, on_delete=models.CASCADE, related_name='goods', verbose_name=_('Товары'))
    comments = models.TextField(max_length=1000, verbose_name=_('Комментарии'))


#
#
# class Price(models.Model):
#     pass