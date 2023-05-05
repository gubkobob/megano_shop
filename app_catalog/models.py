from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()


class Products(models.Model):
    pass


class Comments(models.Model):
    goods = models.OneToOneField(Products, on_delete=models.CASCADE, related_name='goods')
    comments = models.TextField(max_length=1000)

    pass

#
#
# class Price(models.Model):
#     pass