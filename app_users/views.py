from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django_jinja.views.generic import CreateView
from django.contrib.auth import get_user_model

from app_users.forms import MyUserCreationForm

User = get_user_model()


class MyLoginView(LoginView):

    template_name = "users/login.html"
    success_url = reverse_lazy("app_users:profile")

    def form_valid(self, form):
        response = super().form_valid(form)

        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")

        user = authenticate(self.request, email=email, password=password)
        if user:
            login(request=self.request, user=user)
        return response

class RegisterView(CreateView):
    # model = User
    form_class = MyUserCreationForm
    # fields = "username", "email", "password"
    template_name = "users/registr.jinja2"

    success_url = reverse_lazy("app_users:profile")

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        email = form.cleaned_data.get("email")


        User.objects.create(username=username, password=password, email=email)
        User.save()
        user = authenticate(self.request, email=email, password=password)
        login(request=self.request, user=user)
        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("app_users:login")


class AboutMeView(TemplateView):
    template_name = "users/profile.html"