from django.dispatch import Signal

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from app_catalog.models import Category, SubCategory, Product

my_signal = Signal()


@receiver(post_save, sender=Product)
def save_cache_product(sender, **kwargs):
    cache.set('products', 'products_cache', 86400)
    print('save_cache_product', cache.get('products'))


@receiver(my_signal, sender=Category)
@receiver(my_signal, sender=SubCategory)
@receiver(my_signal, sender=Product)
def delete_cache_product(sender, **kwargs):
    if sender == Category:
        cache.delete('categories')
        print('delete_cache_categories')
    elif sender == SubCategory:
        cache.delete('subcategories')
        print('delete_cache_subcategories')
    elif sender == Product:
        cache.delete('products')
        print('delete_cache_product')
