from django.views.generic import ListView

from .models import Discount
from .services import DiscountsServicesMixin


class DiscountView(ListView):
    model = Discount
    template_name = "shops/sale.jinja2"
    paginate_by = 3
    context_object_name = "discounts"

    def get_context_data(self, **kwargs):
        discount = DiscountsServicesMixin()
        context = super().get_context_data(**kwargs)
        result = discount.get_discounts_page()
        return dict(context.items())

    def get_queryset(self):
        return Discount.objects.filter(available=True)
