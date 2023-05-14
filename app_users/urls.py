from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    MyLogoutView,
    RegisterView, AboutMeView, MyLoginView,
)

app_name = "app_users"

urlpatterns = [
    path("profile/", AboutMeView.as_view(), name="profile"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        MyLoginView.as_view(redirect_authenticated_user=True), name="login"),
    # path("login/", login_view, name="login"),

    path("logout/", MyLogoutView.as_view(), name="logout"),
]
