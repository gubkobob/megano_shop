from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
# from .models import Discount


class AppDiscountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_discounts"
    verbose_name = _('Скидки')

    # def ready(self):
    #     for _ in Discount.objects.get_queryset():
    #         _.available_monitoring()
    #     from app_discounts import signals
    #     # pass