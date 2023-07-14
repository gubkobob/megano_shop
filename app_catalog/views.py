from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.db.models import Max
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from app_cart.forms import CartAddProductInShopForm
from .models import ProductInShop, Comments, Specifications, Subspecifications
from .services import sort_catalog, paginator, filter_catalog


class CategoryView(ListView):
    """Представление категорий"""
    queryset = ProductInShop.objects.prefetch_related('product_discount')
    template_name = 'app_catalog/catalog.jinja2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request.GET
        result = sort_catalog(request)
        catalog_obj = result.get('productsinshops')
        context['sort'] = result.get('sort')
        maxprice = ProductInShop.objects.aggregate(Max('price'))
        popular_tags = ProductInShop.objects.order_by('product__subcategory')[:4]
        context['maxprice'] = maxprice.get("price__max")
        context['popular_tags'] = popular_tags

        # Paginator
        catalog_page_obj = paginator(obj=catalog_obj, request=request)
        context['catalog_page_obj'] = catalog_page_obj
        context['productsinshops'] = catalog_page_obj.object_list
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
                                          'productsinshops': catalog_page_obj.object_list,
                                          'catalog_page_obj': catalog_page_obj,
                                      }
                          )


class ProductInShopDetailView(DetailView, FormMixin):
    queryset = ProductInShop.objects\
        .select_related("product")\
        .prefetch_related("images_in_shop")\
        .prefetch_related("comments")
    template_name = 'app_catalog/product_details.jinja2'
    context_object_name = "product_in_shop"
    form_class = CartAddProductInShopForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        product = ProductInShop.objects.get(pk=self.kwargs.get('pk')).product
        specifications = Specifications.objects.filter(product=product).all()
        subspecifications = Subspecifications.objects.filter(specification__in=specifications).all()
        context['specifications'] = subspecifications
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if request.method == "POST":
            user = request.user
            text_comment = request.POST.get('review')
            if text_comment:
                if user == AnonymousUser():
                    messages.add_message(request, messages.ERROR, "Для оставления отзыва нужно зарегистрироваться")
                else:
                    product_in_shop = ProductInShop.objects.get(pk=pk)
                    new_comment = Comments.objects.create(user=user, comment=text_comment, product_in_shop=product_in_shop)
                    new_comment.save()
            return redirect('appcatalog:product_details', pk=pk)

