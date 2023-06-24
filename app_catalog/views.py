import datetime
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from app_administrator.models import SettingsModel
from .models import ProductInShop, Comments
from .services import sort_catalog, paginator, filter_catalog


class CategoryView(ListView):
    """Представление категорий"""
    model = ProductInShop
    template_name = 'app_catalog/catalog.jinja2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request.GET
        result = sort_catalog(request)
        catalog_obj = result.get('productsinshops')
        context['sort'] = result.get('sort')
        context['productsinshops'] = catalog_obj
        return context

    def post(self, request):
        if request.method == "POST":
            post = request.POST
            catalog_obj = filter_catalog(post)

            # Paginator
            # req = self.request.GET
            # catalog_page_obj = paginator(obj=catalog_obj, request=req)
            return render(request, 'app_catalog/catalog.jinja2',
                          context={
                              'productsinshops': catalog_obj
                              # 'catalog_page_obj': catalog_page_obj
                          }
                          )

# class CategoryView2(ListView):
#     """Представление категорий"""
#     model = ProductInShop
#     template_name = 'app_catalog/catalog.jinja2'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         request = self.request.GET
#         result = sort_catalog(request)
#         catalog_obj = result.get('productsinshop')
#         context['sort'] = result.get('sort')
#
#         # Paginator
#         catalog_page_obj = paginator(obj=catalog_obj, request=request)
#         context['catalog_page_obj'] = catalog_page_obj
#         context['productsinshops'] = catalog_page_obj.object_list
#         return context
#
#     def post(self, request):
#         if request.method == "POST":
#             post = request.POST
#             catalog_obj = filter_catalog(post)
#
#             # Paginator
#             req = self.request.GET
#             catalog_page_obj = paginator(obj=catalog_obj, request=req)
#             return render(request, 'app_catalog/catalog.jinja2',
#                           context={
#                               'products': catalog_page_obj.object_list,
#                               'catalog_page_obj': catalog_page_obj
#                           }
#                           )


class ProductInShopDetailView(DetailView):
    model = ProductInShop
    template_name = 'app_catalog/product_details.jinja2'
    context_object_name = "product_in_shop"
#
#     def get_context_data(self, **kwargs):
#
#         context = super().get_context_data(**kwargs)
#         product = Product.objects.get(pk=self.kwargs.get('pk'))
#         comments = Comments.objects.filter(goods=product)
#         context['comments'] = comments
#         return context
#
#     def post(self, request, pk=None):
#         if request.method == "POST":
#             text_comment = request.POST.get('review')
#             user = request.user
#             product = Product.objects.get(pk=pk)
#             new_comment = Comments.objects.create(user=user, comment=text_comment, goods = product)
#             new_comment.save()
#             comments = Comments.objects.filter(goods=product)
#             return render(request, 'app_catalog/product_details.jinja2',
#                           context={
#                               'comments': comments,
#                               'product': product,
#                           }
#                           )
