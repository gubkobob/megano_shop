from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from app_catalog.models import Category, SubCategory, Product


@receiver(signal=post_save, sender=Category)
def post_save_cache_categories(sender, **kwargs):
    if kwargs.get('created'):
        cache.set('categories', 'categories_cache', 86400)


@receiver(signal=post_delete, sender=Category)
def post_delete_cache_categories(sender, **kwargs):
    cache.delete('categories')


@receiver(signal=post_save, sender=SubCategory)
def post_save_cache_subcategories(sender, **kwargs):
    if kwargs.get('created'):
        cache.set('subcategories', 'subcategories_cache', 86400)


@receiver(signal=post_delete, sender=SubCategory)
def post_delete_cache_subcategories(sender, **kwargs):
    cache.delete('subcategories')


@receiver(post_save, sender=Product)
def post_save_cache_products(sender, **kwargs):
    if kwargs.get('created'):
        cache.set('products', 'products_cache', 86400)


@receiver(signal=post_delete, sender=Product)
def post_delete_cache_products(sender, **kwargs):
    cache.delete('products')
