from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Category, Product, ProductImage, SubCategory
from app_administrator.models import SettingsModel


def categories_list(request, category_slug=None, subcategory_slug=None):
    """ отображение на странице категорий, подкатегорий, продуктов - доступных для заказа"""
    cache_time = getattr(SettingsModel.objects.first(), 'cache_time')
    category = None
    subcategory = None
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.filter(products__isnull=False).distinct()
        cache.set('categories', categories, cache_time)
    subcategories = cache.get('subcategories')
    if not subcategories:
        subcategories = SubCategory.objects.filter(category__isnull=False, products__isnull=False).distinct()
        cache.set('subcategories', subcategories, cache_time)
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    if subcategory_slug:
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
        products = products.filter(subcategory=subcategory)

    return render(request,
                  'app_catalog/catalog.jinja2',
                  {'category': category,
                   'categories': categories.order_by('id'),
                   'products': products,
                   'subcategory': subcategory,
                   'subcategories': subcategories.order_by('id')
                   })
