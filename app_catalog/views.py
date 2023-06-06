from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import Category, Product, ProductImage, SubCategory
from django.template.response import TemplateResponse

from .services import sort_catalog


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


class CategoryCreateView(CreateView):
    """ создать категорию и очистить кеш """
    cache.clear()
    model = Category
    fields = "name",
    success_url = reverse_lazy('appcatalog:categories_list')


class CategoryUpdateView(UpdateView):
    """ изменить категорию и очистить кеш """
    cache.clear()
    model = Category
    fields = "name",
    success_url = reverse_lazy('appcatalog:categories_list')


class CategoryDeleteView(DeleteView):
    """ удалить категорию и очистить кеш"""
    cache.clear()
    model = Category
    success_url = reverse_lazy('appcatalog:categories_list')


class SubCategoryCreateView(CreateView):
    """ создать подкатегорию и очистить кеш"""
    cache.clear()
    model = SubCategory
    fields = "name",
    success_url = reverse_lazy('appcatalog:categories_list')


class SubCategoryUpdateView(UpdateView):
    """ создать подкатегорию и очистить кеш"""
    cache.clear()
    model = SubCategory
    fields = "name",
    success_url = reverse_lazy('appcatalog:categories_list')


class SubCategoryDeleteView(DeleteView):
    """ создать подкатегорию и очистить кеш"""
    cache.clear()
    model = SubCategory
    success_url = reverse_lazy('appcatalog:categories_list')

class CategoryView(ListView):
    """Представление категорий"""
    model = Product
    template_name = 'app_catalog/catalog.jinja2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context['products'] = products
        return context

    def get(self, request):
        context = sort_catalog(request.GET)
        return render(request, 'app_catalog/catalog.jinja2',
                      context=context)

    def post(self, request):
        if request.method == "POST":
            price_filter = request.POST.get('price').split(';')
            min_price_filter = int(price_filter[0])
            max_price_filter = int(price_filter[1])
            products = Product.objects.filter(price__gte=min_price_filter, price__lte=max_price_filter)
            # return HttpResponseRedirect('/catalog')
            return render(request, 'app_catalog/catalog.jinja2',
                          context={'products': products})

