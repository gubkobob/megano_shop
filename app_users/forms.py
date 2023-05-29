from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class MyUserCreationForm(UserCreationForm):
   class Meta:
      model = User
      fields = ('username', 'email', 'password1', 'password2')


class MyUserChangeForm(forms.Form):
   username = forms.CharField(required=False)
   email = forms.EmailField(required=False)
   phone_number = forms.IntegerField(required=False)
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
#    phone_number = forms.IntegerField(required=False)
#
#    class Meta:
#       model = User
#       fields = ('username', 'email', 'avatar')
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


