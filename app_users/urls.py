from django.contrib.auth.views import LoginView
from django.urls import path

from .views import MyLogoutView, RegisterView, ProfileView, MyLoginView, AccountView

app_name = "app_users"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("account/", AccountView.as_view(), name="account"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", MyLoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
]
