from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppAdministratorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_administrator"
    verbose_name = _("Административное меню")

    def ready(self):
        from app_administrator import signals
