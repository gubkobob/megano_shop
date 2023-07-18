from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppDiscountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_discounts"
    verbose_name = _("Скидки")