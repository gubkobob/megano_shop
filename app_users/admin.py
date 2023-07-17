from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "date_joined",
        "is_active",
        "avatar",
    )
    list_display_links = "first_name", "email"
    ordering = ("pk",)
