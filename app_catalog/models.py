from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Category(models.Model):
    """Модель категорий каталога"""

    name = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        db_index=True,
        verbose_name="Название категории",
    )
    slug = models.SlugField(
        max_length=100,
        null=False,
        blank=True,
        unique=True,
        verbose_name="URL категории",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name", "slug"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("appcatalog:categories_list_with_products", args=[self.slug])


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="subcategory",
    )
    name = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        db_index=True,
        verbose_name="Название подкатегории",
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Shop(models.Model):
    """Модель магазина"""

    name = models.CharField(max_length=100)
    descriptions = models.TextField()
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField(
        null=True, blank=True, default="no_photo.jpg", verbose_name="Логотип"
    )
    product = models.ManyToManyField(to="Product", through="ProductInShop")

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
        ordering = [
            "name",
        ]
        index_together = [
            ("id",),
        ]

    def __str__(self) -> str:
        return f"{self.name}"


class Product(models.Model):
    """Модель товаров"""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Название категории",
        related_name="products",
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        verbose_name="Название подкатегории",
        related_name="products",
    )
    name = models.CharField(
        max_length=200, db_index=True, verbose_name="Название товара"
    )
    description = models.TextField(blank=True, verbose_name="Описание товара")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания товара"
    )
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления товара")
    image_main = models.ImageField(
        null=True, blank=True, default="no_photo.jpg", verbose_name="Картинка"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class ProductInShop(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="products_in_shop",
        on_delete=models.CASCADE,
        verbose_name=_("Название"),
    )
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="products_in_shop"
    )
    quantity = models.PositiveIntegerField(
        default=0, verbose_name=_("Количество товара")
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена товара"
    )
    available = models.BooleanField(default=True, verbose_name="Доступность товара")
    limited_product = models.BooleanField(
        default=False, verbose_name="Ограниченный тираж"
    )

    class Meta:
        verbose_name = "Магазины и их товары"
        verbose_name_plural = "Магазины и их товары"
        ordering = ["-id", "shop", "product", "price"]

    def __str__(self):
        return self.product.name


def product_in_shop_images_directory_path(
    instance: "ProductInShopImage", filename: str
) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product_in_shop.pk,
        filename=filename,
    )


class ProductInShopImage(models.Model):
    """Модель картинок к товарам"""

    product_in_shop = models.ForeignKey(
        ProductInShop,
        on_delete=models.CASCADE,
        related_name="images_in_shop",
        verbose_name="Товар",
    )
    image = models.ImageField(
        upload_to=product_in_shop_images_directory_path, verbose_name="Картинка"
    )

    class Meta:
        verbose_name = "Картинка товара"
        verbose_name_plural = "Картинки товаров"


class Comments(models.Model):
    product_in_shop = models.ForeignKey(
        ProductInShop,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Товары"),
    )
    comment = models.TextField(max_length=1000, verbose_name=_("Комментарии"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Пользователь")
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания отзыва"
    )
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления отзыва")

    class Meta:
        verbose_name = "Отзыв к товару"
        verbose_name_plural = "Отзывы к товару"


class Specifications(models.Model):
    """Модель характеристик"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="specification",
        verbose_name=_("Товар"),
    )
    name_specification = models.TextField(
        max_length=40, verbose_name=_("Название характеристики")
    )

    class Meta:
        verbose_name = "Характеристика товара"
        verbose_name_plural = "Характеристики товара"

    def __str__(self):
        return self.name_specification


class Subspecifications(models.Model):
    """Модель значений характеристик"""

    specification = models.ForeignKey(
        Specifications,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subspecification",
        max_length=1000,
        verbose_name=_("Характеристика"),
    )
    name_subspecification = models.TextField(
        max_length=100, verbose_name=_("Название характеристики")
    )
    text_subspecification = models.TextField(
        max_length=100, verbose_name=_("Текст Характеристики")
    )

    class Meta:
        verbose_name = "Значение характеристики"
        verbose_name_plural = "Значения характеристик"

    def __str__(self):
        return self.name_subspecification
