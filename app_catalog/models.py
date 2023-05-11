from django.db import models


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