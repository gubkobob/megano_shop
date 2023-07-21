from django.views.generic import ListView

from .models import Discount
from .services import DiscountsServicesMixin


class DiscountView(ListView):
    """Функция отображения Скидок"""
    model = Discount
    template_name = "shops/sale.jinja2"
    paginate_by = 3
    context_object_name = "discounts"

    def get_context_data(self, **kwargs):

        # отправка всех объектов
        discount = DiscountsServicesMixin()
        context = super().get_context_data(**kwargs)

        # проверка скидок на истекщий срок
        result = discount.get_discounts_page()
        return dict(context.items())

    def get_queryset(self):
        """Функция получения списка объектов скидок с фильтрацией по активной скидке(рабочей)"""
        return Discount.objects.filter(available=True)
