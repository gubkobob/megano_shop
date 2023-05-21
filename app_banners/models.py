from django.db import models
class Banner(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Settings(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.key
