from django.shortcuts import render
from django.views.generic import ListView, DetailView

from app_catalog.services import paginator
from .models import Discount
from .services import DiscountsServicesMixin


class DiscountView(ListView):
    model = Discount
    template_name = 'shops/sale.jinja2'

    def get_context_data(self, **kwargs):
        discount = DiscountsServicesMixin()
        # context = super().get_context_data(**kwargs)
        request = self.request.GET
        context = {}

        result = discount.get_discounts_page()
        context['context'] = result
        catalog_page_obj = paginator(obj=result, request=request)
        context['catalog_page_obj'] = catalog_page_obj
        return context
