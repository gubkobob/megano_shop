from app_catalog.models import Product
from django.db import models


class Banner(models.Model):
    """Модель банера"""
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="banners/")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
