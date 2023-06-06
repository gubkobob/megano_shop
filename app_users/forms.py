from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django import forms

from app_users.validators import phone_validator, same_phone_validate, file_size, email_exist_validator

User = get_user_model()


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

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

    password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ("username", "email", "avatar", "phone_number")

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        self.fields["phone_number"].validators = [
            phone_validator,
        ]  # same_phone_validate, ]
        self.fields["avatar"].validators = [file_size, ]
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


# class UserForgotPasswordForm(forms.Form):
#     email = forms.EmailField(max_length=50, required=True)
#
#
# class UserSetNewPasswordForm(forms.Form):
#     password1 = forms.CharField(widget=forms.PasswordInput(), required=True)
#     password2 = forms.CharField(widget=forms.PasswordInput(), required=True)


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
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
        self.fields["email"].validators = [email_exist_validator, ]


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
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
