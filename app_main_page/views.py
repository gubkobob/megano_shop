from django.shortcuts import render
from django.utils import timezone
from app_catalog.models import Product
from django.db.models import Sum


def main_page(request):
    top_products = Product.objects.annotate(quantity_sum=Sum('order_items__quantity')).order_by('-quantity_sum')[:6] #популярные товары (по продажам)
    products_limited = Product.objects.all().order_by('stock')[:9] #ограниченный тираж
    products_limited_offers = Product.objects.all().order_by('?')[:1] #ограниченные предложения
    time_action = timezone.now()

    return render(request,
                  'app_main_page/main.jinja2',
                  {
                      'top_products':  top_products,
                      'products_limited': products_limited,
                      'limited_offers': products_limited_offers,
                      'time_action': time_action
                  })
