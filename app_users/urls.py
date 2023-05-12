# from django.contrib.auth.views import LoginView
# from django.urls import path

# from .views import (
#     MyLogoutView,
#     RegisterView,
# )
#
# app_name = "app_users"
#
# urlpatterns = [
#     # path("register/", RegisterView.as_view(), name="register"),
#     path(
#         "login/",
#         LoginView.as_view(
#             template_name="app_users/login.html", redirect_authenticated_user=True
#         ),
#         name="login",
#     ),
#     path("logout/", MyLogoutView.as_view(), name="logout"),
# ]
