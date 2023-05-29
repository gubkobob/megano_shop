from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django_jinja.views.generic import CreateView, UpdateView
from django.contrib.auth import get_user_model

from app_users.forms import MyUserCreationForm, MyUserChangeForm

User = get_user_model()


class MyLoginView(LoginView):

    template_name = "users/login.jinja2"
    success_url = reverse_lazy("app_users:profile")


class RegisterView(CreateView):

    form_class = MyUserCreationForm
    template_name = "users/registr.jinja2"
    success_url = reverse_lazy("app_users:profile")

    # def get(self, request: HttpRequest) -> HttpResponse:
    #     if self.request.user.is_authenticated:
    #         return render(request, 'users/profile.jinja2')

    def form_valid(self, form):
        response = super().form_valid(form)

        password = form.cleaned_data.get("password1")
        email = form.cleaned_data.get("email")

        user = authenticate(self.request, email=email, password=password)
        login(request=self.request, user=user)
        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("app_users:login")


# class ProfileView(UpdateView):
#     model = User
#     fields = ('username', 'email', 'avatar', 'phone_number', 'password')
#     queryset = User.objects.filter(pk=1)
#     # form_class = MyUserChangeForm
#     template_name = "users/profile.jinja2"
#     success_url = reverse_lazy("app_users:profile")

class ProfileView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": MyUserChangeForm(),
            "user": self.request.user,
        }
        return render(request, 'users/profile.jinja2', context=context)

    def post(self, request: HttpRequest):
        form = MyUserChangeForm(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.filter(pk=request.user.pk).all()[0]
            if form.cleaned_data["username"]:
                user.username = form.cleaned_data["username"]
            if form.cleaned_data["phone_number"]:
                user.phone_number = form.cleaned_data["phone_number"]
            if form.cleaned_data["email"]:
                user.email = form.cleaned_data["email"]
            if form.cleaned_data["avatar"]:
                user.avatar = form.cleaned_data["avatar"]
            if form.cleaned_data["password1"] and form.cleaned_data["password2"] and form.cleaned_data["password1"] == form.cleaned_data["password2"]:
                user.set_password(form.cleaned_data["password1"])
                user.save()
                user = authenticate(self.request, email=form.cleaned_data["email"], password=form.cleaned_data["password1"])
                login(request=self.request, user=user)

            user.save()
        print(form.errors)
        return redirect(request.path)


class AccountView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "user": self.request.user,
        }
        return render(request, 'users/account.jinja2', context=context)

