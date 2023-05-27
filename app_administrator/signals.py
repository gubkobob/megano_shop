from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from app_catalog.models import Category, SubCategory, Product


@receiver(signal=pre_save, sender=Category)
def pre_save_cache_categories(sender, **kwargs):
    cache.set('categories', 'categories_cache', 86400)
    print('categories pre save')


@receiver(signal=post_save, sender=Category)
def post_save_cache_categories(sender, **kwargs):
    if kwargs.get('created'):
        cache.set('categories', 'categories_cache', 86400)
        print('categories post save')


@receiver(signal=pre_delete, sender=Category)
def pre_delete_cache_categories(sender, **kwargs):
    cache.delete('categories')
    print('categories pre del')


@receiver(signal=post_delete, sender=Category)
def post_delete_cache_categories(sender, **kwargs):
    cache.delete('categories')
    print('categories post del')


@receiver(signal=pre_save, sender=SubCategory)
def pre_save_cache_subcategories(sender, **kwargs):
    cache.set('subcategories', 'subcategories_cache', 86400)
    print('subcategories pre save')


@receiver(signal=post_save, sender=SubCategory)
def post_save_cache_subcategories(sender, **kwargs):
    if kwargs.get('created'):
        cache.set('subcategories', 'subcategories_cache', 86400)
        print('subcategories post save')


@receiver(signal=pre_delete, sender=SubCategory)
def pre_delete_cache_subcategories(sender, **kwargs):
    cache.delete('subcategories')
    print('subcategories pre del')


@receiver(signal=post_delete, sender=SubCategory)
def post_delete_cache_subcategories(sender, **kwargs):
    cache.delete('subcategories')
    print('subcategories post del')


@receiver(pre_save, sender=Product)
def pre_save_cache_products(sender, **kwargs):
    cache.set('products', 'products_cache', 86400)
    print('products pre save')


@receiver(post_save, sender=Product)
def post_save_cache_products(sender, **kwargs):
    if kwargs.get('created'):
        cache.set('products', 'products_cache', 86400)
        print('products post save')


@receiver(signal=pre_delete, sender=Product)
def pre_delete_cache_products(sender, **kwargs):
    cache.delete('products')
    print('products pre del')


@receiver(signal=post_delete, sender=Product)
def post_delete_cache_products(sender, **kwargs):
    cache.delete('products')
    print('products post del')
