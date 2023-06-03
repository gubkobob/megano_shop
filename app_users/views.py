from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView
from django_jinja.views.generic import CreateView, UpdateView
from django.contrib.auth import get_user_model
from app_users.forms import MyUserCreationForm, MyUserChangeForm
from app_users.services import reset_phone_format

User = get_user_model()


class MyLoginView(LoginView):

    template_name = "users/login.jinja2"
    success_url = reverse_lazy("app_users:profile")


class RegisterView(CreateView):

    form_class = MyUserCreationForm
    template_name = "users/registr.jinja2"
    success_url = reverse_lazy("app_users:profile")

    def form_valid(self, form):
        response = super().form_valid(form)

        password = form.cleaned_data.get("password1")
        email = form.cleaned_data.get("email")

        user = authenticate(self.request, email=email, password=password)
        login(request=self.request, user=user)
        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("app_users:login")


class ProfileView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": MyUserChangeForm(),
            "user": request.user,
        }
        return render(request, "users/profile.jinja2", context=context)

    def post(self, request: HttpRequest):
        form = MyUserChangeForm(request.POST, request.FILES, instance=request.user)
        context = {
            "form": form,
            "user": request.user,
        }
        if form.is_valid():
            form.save()
            reset_phone_format(request.user)
            if (
                form.cleaned_data["password1"]
                and form.cleaned_data["password2"]
                and form.cleaned_data["password1"] == form.cleaned_data["password2"]
            ):
                user = request.user
                user.set_password(form.cleaned_data["password1"])
                user.save()
                user = authenticate(
                    request,
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password1"],
                )
                login(request=request, user=user)
            messages.add_message(request, messages.SUCCESS, "Профиль успешно сохранен")

        return render(request, "users/profile.jinja2", context=context)


class AccountView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "user": request.user,
        }
        return render(request, "users/account.jinja2", context=context)
