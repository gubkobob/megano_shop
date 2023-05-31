from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.validators import RegexValidator


User = get_user_model()
phone_validator = RegexValidator(r"^\d{10}$", "Телефон должен быть 10 цифр без кода страны!")

class MyUserCreationForm(UserCreationForm):
   class Meta:
      model = User
      fields = ('username', 'email', 'password1', 'password2')

   def clean(self):
      cleaned_data = super(MyUserCreationForm, self).clean()
      password1 = cleaned_data.get("password1")
      password2 = cleaned_data.get("password2")

      if password1 != password2:
         raise forms.ValidationError(
            "password and confirm_password does not match"
         )
      return cleaned_data


class MyUserChangeForm(forms.Form):
   username = forms.CharField(required=False, max_length=30)
   email = forms.EmailField(required=False)
   phone_number = forms.CharField(required=False, max_length=10, validators=[phone_validator, ])
   avatar = forms.ImageField(required=False)
   password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
   password2 = forms.CharField(widget=forms.PasswordInput(), required=False)

   def clean(self):
      cleaned_data = super(MyUserChangeForm, self).clean()
      password1 = cleaned_data.get("password1")
      password2 = cleaned_data.get("password2")

      if password1 != password2:
         raise forms.ValidationError(
            "password and confirm_password does not match"
         )
      return cleaned_data


# class MyUserChangeForm(forms.ModelForm):
#
#    password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
#    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)
#
#    class Meta:
#       model = User
#       fields = ('username', 'email', 'avatar', 'phone_number')
#
#    def clean(self):
#       cleaned_data = super(MyUserChangeForm, self).clean()
#       password1 = cleaned_data.get("password1")
#       password2 = cleaned_data.get("password2")
#
#       if password1 != password2:
#          raise forms.ValidationError(
#             "password and confirm_password does not match"
#          )
      # return cleaned_data

