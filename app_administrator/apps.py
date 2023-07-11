from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
# from django.core.signals import pre_save, post_migrate


class AppAdministratorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_administrator"
    verbose_name = _('Административное меню')

    # def register_signals(self, **kwargs):
    #     from . import signals
    #
    # def ready(self):
    #     post_migrate.connect(self.register_signals, sender=self)

    def ready(self):
        from app_administrator import signals
