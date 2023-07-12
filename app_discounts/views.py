from django.shortcuts import render
from django.views.generic import ListView, DetailView

from django.core.paginator import Paginator
from .models import Discount
from .services import DiscountsServicesMixin


class DiscountView(ListView):
    model = Discount
    template_name = 'shops/sale.jinja2'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        discount = DiscountsServicesMixin()
        # context = super().get_context_data(**kwargs)
        request = self.request.GET
        context = {}

        result = discount.get_discounts_page()
        # print(result[:])
        context['context'] = result
        paginator = Paginator(result, self.paginate_by)
        page = self.request.GET.get('page')
        # print(page)
        file_exams = paginator.get_page(page)
        # context['context'] = file_exams
        # catalog_page_obj = paginator(obj=result, request=request)
        # context['catalog_page_obj'] = catalog_page_obj
        return context
