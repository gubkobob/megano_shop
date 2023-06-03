from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

from app_users.validators import phone_validator, same_phone_validate

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
