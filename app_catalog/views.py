import datetime
from django.shortcuts import render
from django.views.generic import ListView
from app_administrator.models import SettingsModel
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


def product_details(request, pk):
    product = Product.objects.get(pk=pk)
    product.last_visit = datetime.datetime.now()
    product.save()
    count_viewed = getattr(SettingsModel.objects.first(), 'count_viewed')
    recently_viewed_products = None
    product_id = pk

    if 'recently_viewed' in request.session:
        if product_id in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(product_id)
        request.session['recently_viewed'].insert(0, product_id)
        recently_viewed_products = Product.objects.filter(pk__in=request.session['recently_viewed']).order_by(
            '-last_visit')
        if len(request.session['recently_viewed']) > count_viewed:
            request.session['recently_viewed'].pop(-1)
    else:
        request.session['recently_viewed'] = [product_id]
    request.session.modified = True
    context = {
        'product': product,
        'recently_viewed_products': recently_viewed_products
    }
    return render(request, 'app_catalog/product_details.jinja2', context)


