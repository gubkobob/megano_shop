from app_users.services import get_10_digits_from_phone_number
from app_users.validators import email_exist_validator, file_size, phone_validator
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)

User = get_user_model()


class MyUserCreationForm(UserCreationForm):
    """
    Форма для создания пользователя
    """

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields["phone_number"].validators = [
            phone_validator,
        ]

    def clean_phone_number(self):
        cleaned_data = super(MyUserCreationForm, self).clean()
        phone_number_10_digits = get_10_digits_from_phone_number(
            cleaned_data.get("phone_number")
        )
        users = User.objects.all()
        for user in users:
            if phone_number_10_digits == user.phone_number:
                msg = "This phone number already used by another user"
                raise forms.ValidationError(msg)
        return cleaned_data.get("phone_number")

    def clean(self):
        cleaned_data = super(MyUserCreationForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("password and confirm_password does not match")
        if password1 and len(password1) < 8:
            raise forms.ValidationError(
                "Your password must contain at least 8 characters."
            )
        return cleaned_data


class MyUserChangeForm(forms.ModelForm):
    """
    Форма изменения данных пользователя
    """

    password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ("username", "email", "avatar", "phone_number")

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        self.fields["phone_number"].validators = [
            phone_validator,
        ]
        self.fields["avatar"].validators = [
            file_size,
        ]

    def clean(self):
        cleaned_data = super(MyUserChangeForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("password and confirm_password does not match")
        if password1 and len(password1) < 8:
            raise forms.ValidationError(
                "Your password must contain at least 8 characters."
            )
        return cleaned_data

    def clean_phone_number(self):
        cleaned_data = super(MyUserChangeForm, self).clean()
        phone_number_10_digits = get_10_digits_from_phone_number(
            cleaned_data.get("phone_number")
        )
        users = User.objects.exclude(pk=self.instance.pk)
        for user in users:
            if phone_number_10_digits == user.phone_number:
                msg = "This phone number already used by another user"
                raise forms.ValidationError(msg)
        return cleaned_data.get("phone_number")


class UserForgotPasswordForm(PasswordResetForm):
    """
    Запрос на восстановление пароля
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super(UserForgotPasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "autocomplete": "off"}
            )
        self.fields["email"].validators = [
            email_exist_validator,
        ]


class UserSetNewPasswordForm(SetPasswordForm):
    """
    Изменение пароля пользователя после подтверждения
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "autocomplete": "off"}
            )
