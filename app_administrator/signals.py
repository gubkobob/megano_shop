from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from app_catalog.models import Category, SubCategory, Product, ProductInShop
from .models import SettingsModel


def get_time_cache():
    try:
        time_cache = getattr(SettingsModel.objects.first(), 'cache_time')
    except Exception as error_signals:
        pass


@receiver(signal=post_save, sender=Category)
def post_save_cache_categories(sender, **kwargs):
    if kwargs.get('created'):
        cache.set('category', 'category_cache', get_time_cache())


@receiver(signal=post_delete, sender=Category)
def post_delete_cache_categories(sender, **kwargs):
    cache.delete('category')


@receiver(signal=post_save, sender=SubCategory)
def post_save_cache_subcategories(sender, **kwargs):
    if kwargs.get('created'):
        cache.set('subcategory', 'subcategory_cache', get_time_cache())


@receiver(signal=post_delete, sender=SubCategory)
def post_delete_cache_subcategories(sender, **kwargs):
    cache.delete('subcategory')


@receiver(post_save, sender=Product)
def post_save_cache_products(sender, **kwargs):
    if kwargs.get('created'):
        cache.set('product', 'product_cache', get_time_cache())


@receiver(signal=post_delete, sender=Product)
def post_delete_cache_products(sender, **kwargs):
    cache.delete('product')


@receiver(post_save, sender=ProductInShop)
def post_save_cache_products_in_shop(sender, **kwargs):
    if kwargs.get('created'):
        cache.set('product_in_shop', 'product_in_shop_cache', get_time_cache())


@receiver(signal=post_delete, sender=ProductInShop)
def post_delete_cache_products_in_shop(sender, **kwargs):
    cache.delete('product_in_shop')
