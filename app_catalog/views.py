from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Category, Product, ProductImage, SubCategory


def categories_list(request, category_slug=None, subcategory_slug=None):
    """ отображение на странице категорий, подкатегорий, продуктов - доступных для заказа"""
    category = None
    subcategory = None
    categories = cache.get('categories')     # берем категорию из кеша
    if not categories:
        # берем только те категории, в которых есть продукты
        categories = Category.objects.filter(products__isnull=False).distinct()
        cache.set('categories', categories, 86400)         # записываем категорию в кеш
    subcategories = cache.get('subcategories')    # берем подкатегорию из кеша
    if not subcategories:
        # берем только те подкатегории, в которых есть продукты
        subcategories = SubCategory.objects.filter(category__isnull=False, products__isnull=False).distinct()
        cache.set('subcategories', subcategories, 86400)          # записываем категорию в кеш
    products = Product.objects.filter(available=True) # берем товар, который есть в наличии
    if category_slug: # отбираем товары выбранной категории по url категории (slug)
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    if subcategory_slug:  # отбираем товары выбранной подкатегории по url категории (slug)
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
        products = products.filter(subcategory=subcategory)

    return render(request,
                  'app_catalog/catalog.jinja2',
                  {'category': category,
                   'categories': categories.order_by('id'), #фильтр отображения по id
                   'products': products,
                   'subcategory': subcategory,
                   'subcategories': subcategories.order_by('id') #фильтр отображения по id
                   })
