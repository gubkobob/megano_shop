from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django_jinja.views.generic import CreateView

from app_users.models import User


class RegisterView(CreateView):
    # form_class = UserCreationForm
    model = User
    fields = "username", "email", "password"
    template_name = "registr.html"
    # success_url = reverse_lazy("app_users:about")

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data.get("name")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        User.objects.create(user=self.object)
        user = authenticate(self.request, email=email, password=password)
        login(request=self.request, user=user)
        return response

#
# class MyLogoutView(LogoutView):
#     next_page = reverse_lazy("app_users:login")
