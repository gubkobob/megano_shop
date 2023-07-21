from _decimal import Decimal
from app_orders.models import Order, OrderItem
from app_users.forms import (
    MyUserChangeForm,
    MyUserCreationForm,
    UserForgotPasswordForm,
    UserSetNewPasswordForm,
)
from app_users.services import reset_phone_format
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django_jinja.views.generic import CreateView

User = get_user_model()


class MyLoginView(LoginView):
    """
    Представление для логина на сайте
    """

    template_name = "users/login.jinja2"
    success_url = reverse_lazy("app_users:profile")


class RegisterView(CreateView):
    """
    Представление для регистрации на сайте
    """

    form_class = MyUserCreationForm
    template_name = "users/registr.jinja2"
    success_url = reverse_lazy("app_users:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        reset_phone_format(user)
        user.save()

        password = form.cleaned_data.get("password1")
        email = form.cleaned_data.get("email")

        user = authenticate(self.request, email=email, password=password)
        login(request=self.request, user=user)
        return response


class MyLogoutView(LogoutView):
    """
    Представление для логаута(выхода) пользователя на сайте
    """

    next_page = reverse_lazy("app_users:login")


class ProfileView(View):
    """
    Представление для вывода и изменения детальной информации о пользователе
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": MyUserChangeForm(),
            "user": request.user,
        }
        return render(request, "users/profile.jinja2", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = MyUserChangeForm(request.POST, request.FILES, instance=request.user)
        context = {
            "form": form,
            "user": request.user,
        }
        if form.is_valid():
            user = form.save(commit=False)
            reset_phone_format(user)

            if (
                form.cleaned_data["password1"]
                and form.cleaned_data["password2"]
                and form.cleaned_data["password1"] == form.cleaned_data["password2"]
            ):
                user.set_password(form.cleaned_data["password1"])

                user1 = authenticate(
                    request,
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password1"],
                )
                login(request=request, user=user1)

            user.save()
            messages.add_message(request, messages.SUCCESS, "Профиль успешно сохранен")

        return render(request, "users/profile.jinja2", context=context)


class AccountView(View):
    """
    Представление для вывода данных аккаунта пользователя
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        last_order = (
            Order.objects.filter(user_id=request.user.id).order_by("created_at").last()
        )
        if last_order:
            last_order_items = OrderItem.objects.filter(order_id=last_order.id)
            get_total_price = sum(
                Decimal(item.price) * item.quantity for item in last_order_items
            )
        else:
            last_order = None
            get_total_price = 0
        context = {
            "user": request.user,
            "last_order": last_order,
            "last_order_total_price": get_total_price,
        }
        return render(request, "users/account.jinja2", context=context)


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """

    form_class = UserForgotPasswordForm
    template_name = "users/e-mail.jinja2"
    success_url = reverse_lazy("app_users:login")
    success_message = (
        "Письмо с инструкцией по восстановлению пароля отправлена на ваш email"
    )
    subject_template_name = "email/password_subject_reset_mail.txt"
    email_template_name = "email/password_reset_mail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Запрос на восстановление пароля"
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """

    form_class = UserSetNewPasswordForm
    template_name = "users/password.jinja2"
    success_url = reverse_lazy("app_users:login")
    success_message = "Пароль успешно изменен. Можете авторизоваться на сайте."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Установить новый пароль"
        return context
