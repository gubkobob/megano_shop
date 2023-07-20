from app_catalog.models import Category, Product, ProductInShop, SubCategory
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import SettingsModel


def get_time_cache():
    try:
        time_cache = getattr(SettingsModel.objects.first(), "cache_time")
    except Exception as error_signals:
        pass


@receiver(signal=post_save, sender=Category)
def post_save_cache_categories(sender, **kwargs):
    """
   функция создает cache при создании нового category
    """
    if kwargs.get("created"):
        cache.set("category", "category_cache", get_time_cache())


@receiver(signal=post_delete, sender=Category)
def post_delete_cache_categories(sender, **kwargs):
    """
    функция очищает cache при удалении category
    """
    cache.delete("category")


@receiver(signal=post_save, sender=SubCategory)
def post_save_cache_subcategories(sender, **kwargs):
    """
     функция создает cache при создании нового subcategory
    """
    if kwargs.get("created"):
        cache.set("subcategory", "subcategory_cache", get_time_cache())


@receiver(signal=post_delete, sender=SubCategory)
def post_delete_cache_subcategories(sender, **kwargs):
    """
    функция очищает cache при удалении subcategory
    """
    cache.delete("subcategory")


@receiver(post_save, sender=Product)
def post_save_cache_products(sender, **kwargs):
    """
    функция создает cache при создании нового product
    """
    if kwargs.get("created"):
        cache.set("product", "product_cache", get_time_cache())


@receiver(signal=post_delete, sender=Product)
def post_delete_cache_products(sender, **kwargs):
    """
    функция очищает cache при удалении product
    """
    cache.delete("product")


@receiver(post_save, sender=ProductInShop)
def post_save_cache_products_in_shop(sender, **kwargs):
    """
    функция создает cache при создании нового product_in_shop
    """
    if kwargs.get("created"):
        cache.set("product_in_shop", "product_in_shop_cache", get_time_cache())


@receiver(signal=post_delete, sender=ProductInShop)
def post_delete_cache_products_in_shop(sender, **kwargs):
    """
    функция очищает cache при удалении product_in_shop
    """
    cache.delete("product_in_shop")
