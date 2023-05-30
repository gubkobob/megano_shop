from django.apps import AppConfig


class AppAdministratorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_administrator"

    def ready(self):
        from app_administrator import signals
