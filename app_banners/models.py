from django.db import models
from app_catalog.models import Product
class Banner(models.Model):
    name = models.CharField(max_length=255)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Settings(models.Model):
    banners = models.ManyToManyField(Banner)
    cached_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key
