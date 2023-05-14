from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django_jinja.views.generic import CreateView

from app_users.models import User


# def login_view(request: HttpRequest) -> HttpResponse:
#     if request.method == "GET":
#         if request.user.is_authenticated:
#             return redirect('/admin/')
#
#         return render(request, 'users/login.html')
#
#     email = request.POST["name"]
#     password = request.POST["pass"]
#
#     user = authenticate(request, email=email, password=password)
#     if user:
#         login(request, user)
#         return redirect("/admin/")
#
#     return render(request, "users/login.html", {"error": "Invalid login data"})


class MyLoginView(LoginView):

    template_name = "users/login.html"
    success_url = reverse_lazy("app_users:profile")

    def form_valid(self, form):
        response = super().form_valid(form)

        password = form.cleaned_data.get("pass")
        email = form.cleaned_data.get("name")

        user = authenticate(self.request, email=email, password=password)
        if user:
            login(request=self.request, user=user)
        return response

class RegisterView(CreateView):
    model = User
    # form_class = UserCreationForm

    fields = "email", "password"
    template_name = "users/registr.html"
    success_url = reverse_lazy("app_users:profile")

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data.get("name")
        password = form.cleaned_data.get("pass")
        email = form.cleaned_data.get("login")
        User.objects.create(username=username, password=password, email=email)
        user = authenticate(self.request, email=email, password=password)
        login(request=self.request, user=user)
        return response

#
class MyLogoutView(LogoutView):
    next_page = reverse_lazy("app_users:login")


class AboutMeView(TemplateView):
    template_name = "users/profile.html"