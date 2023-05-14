from django.db import models
from django.urls import reverse


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

#
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


class ProductImage(models.Model):
    """ Модель картинок к товарам """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    image = models.ImageField(verbose_name='Картинка')

    class Meta:
        verbose_name = 'Картинка товара'
        verbose_name_plural = 'Картинки товаров'

# class Shop(models.Model):
#     """Модель магазина"""
#     name = models.CharField(max_length=100)
#     descriptions = models.TextField()
#     address = models.CharField(max_length=100)
#     phone = models.CharField(max_length=20)
#     email = models.EmailField()
#     image = models.ImageField()
#     product = models.ManyToManyField(to="Products", through='ShopsProducts')
#
#     def __str__(self) -> str:
#         return f"{self.name}"
