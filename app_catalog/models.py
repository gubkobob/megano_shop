from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Category(models.Model):
    """ Модель категорий каталога """
    name = models.CharField(max_length=100, null=False, blank=True, db_index=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, null=False, blank=True, unique=True, verbose_name='URL категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name', 'slug']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('appcatalog:categories_list', args=[self.slug])


def product_image_directory_path(instance: 'Product', filename: str) -> str:
    """Фукнция директории изображения продукта
    возвращает айди продукта и имя файла
    """
    return 'products/product_{pk}/image/{filename}'.format(
        pk=instance.pk,
        filename=filename
    )


class Product(models.Model):
    """ Модель товаров """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название товара')
    slug = models.SlugField(max_length=200, db_index=True, verbose_name='URL товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    stock = models.PositiveIntegerField(verbose_name='Остаток товара')
    available = models.BooleanField(default=True, verbose_name='Доступность товара')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания товара')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления товара')
    image = models.ImageField(null=True, blank=True, verbose_name='Картинка')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name', 'slug']
        index_together = [('id', 'slug'), ]

    def __str__(self):
        return self.name


class ProductInShop(models.Model):
    name = models.ManyToManyField(Product, max_length=100, related_name='product', verbose_name=_('Название'))
    price = models.FloatField(default=0, verbose_name=_('Цена'))
    quantity = models.DecimalField(default=0, max_length=255, verbose_name=_('Количество товара'))


class Comments(models.Model):
    goods = models.ManyToManyField(Product, on_delete=models.CASCADE, related_name='goods', verbose_name=_('Товары'))
    comments = models.TextField(max_length=1000, verbose_name=_('Комментарии'))
    user = models.CharField(User, verbose_name=_('Пользователь'))


class ProductImage(models.Model):
    """ Модель картинок к товарам """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    image = models.ImageField(upload_to=product_image_directory_path, verbose_name='Картинка')

    class Meta:
        verbose_name = 'Картинка товара'
        verbose_name_plural = 'Картинки товаров'


class Shop(models.Model):
    """Модель магазина"""
    name = models.CharField(max_length=100)
    descriptions = models.TextField()
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField()
    product = models.ManyToManyField(to="Products", through='ShopsProducts')

    def __str__(self) -> str:
        return f"{self.name}"