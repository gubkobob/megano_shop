from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Category, Product, ProductImage, SubCategory


def categories_list(request, category_slug=None, subcategory_slug=None):
    category = None
    subcategory = None
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.filter(products__isnull=False).distinct()
        cache.set('categories', categories, 86400)
    subcategories = cache.get('subcategories')
    if not subcategories:
        subcategories = SubCategory.objects.filter(category__isnull=False, products__isnull=False).distinct()
        cache.set('subcategories', subcategories, 86400)
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    if subcategory_slug:
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
        products = products.filter(subcategory=subcategory)

    return render(request,
                  'app_catalog/catalog.html',
                  {'category': category,
                   'categories': categories.order_by('id'),
                   'products': products,
                   'subcategory': subcategory,
                   'subcategories': subcategories.order_by('id')
                   })


class CategoryCreateView(CreateView):
    cache.clear()
    model = Category
    fields = "name",
    success_url = reverse_lazy('appcatalog:categories_list')


class CategoryUpdateView(UpdateView):
    cache.clear()
    model = Category
    fields = "name",
    success_url = reverse_lazy('appcatalog:categories_list')


class CategoryDeleteView(DeleteView):
    cache.clear()
    model = Category
    success_url = reverse_lazy('appcatalog:categories_list')


class SubCategoryCreateView(CreateView):
    cache.clear()
    model = SubCategory
    fields = "name",
    success_url = reverse_lazy('appcatalog:subcategories_list')


class SubCategoryUpdateView(UpdateView):
    cache.clear()
    model = SubCategory
    fields = "name",
    success_url = reverse_lazy('appcatalog:subcategories_list')


class SubCategoryDeleteView(DeleteView):
    cache.clear()
    model = SubCategory
    success_url = reverse_lazy('appcatalog:subcategories_list')