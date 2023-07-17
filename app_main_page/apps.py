from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppMainPageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_main_page"
    verbose_name = _("Главная страница")
