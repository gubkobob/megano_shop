from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Category, Product, ProductImage


def categories_list(request, category_slug=None):
    category = None
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.filter(products__isnull=False).distinct()
        cache.set('categories', categories, 86400)
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'app_catalog/catalog.html',
                  {'category': category,
                   'categories': categories.order_by('id'),
                   'products': products
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
