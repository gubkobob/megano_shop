# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.views import LogoutView
# from django.shortcuts import render
# from django.urls import reverse_lazy
# from django_jinja.views.generic import CreateView


# class RegisterView(CreateView):
#     form_class = UserCreationForm
#     template_name = "app_users/register.html"
#     # success_url = reverse_lazy("app_users:about-me")
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         Profile.objects.create(user=self.object)
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password1")
#         user = authenticate(self.request, username=username, password=password)
#         login(request=self.request, user=user)
#         return response

#
# class MyLogoutView(LogoutView):
#     next_page = reverse_lazy("app_users:login")
