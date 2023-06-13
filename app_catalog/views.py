from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import Category, Product, ProductImage, SubCategory
from django.template.response import TemplateResponse
from django.core.cache import cache

from .services import sort_catalog, paginator, filter_catalog


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
        request = self.request.GET
        result = sort_catalog(request)
        catalog_obj = result.get('products')
        context['sort'] = result.get('sort')

        # Paginator
        catalog_page_obj = paginator(obj=catalog_obj, request=request)
        context['catalog_page_obj'] = catalog_page_obj
        context['products'] = catalog_page_obj.object_list
        return context


    def post(self, request):
        if request.method == "POST":
            post = request.POST
            catalog_obj = filter_catalog(post)

            # Paginator
            req = self.request.GET
            catalog_page_obj = paginator(obj=catalog_obj, request=req)
            return render(request, 'app_catalog/catalog.jinja2',
                          context={
                              'products': catalog_page_obj.object_list,
                              'catalog_page_obj': catalog_page_obj
                          }
                          )

