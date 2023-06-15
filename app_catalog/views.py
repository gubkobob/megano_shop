from django.shortcuts import render
from django.views.generic import DetailView, ListView

from app_cart.services import CartServicesMixin
from .models import Product
from .services import sort_catalog, paginator, filter_catalog

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


class ProductCartDetailView(DetailView):
    model = Product
    template_name = 'app_catalog/product_details.jinja2'

