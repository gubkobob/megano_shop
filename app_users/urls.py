from django.urls import path

from .views import (
    AccountView,
    MyLoginView,
    MyLogoutView,
    ProfileView,
    RegisterView,
    UserForgotPasswordView,
    UserPasswordResetConfirmView,
)

app_name = "app_users"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("account/", AccountView.as_view(), name="account"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", MyLoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("password_reset/", UserForgotPasswordView.as_view(), name="password_reset"),
    path(
        "set_new_password/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
