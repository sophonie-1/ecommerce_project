from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy



class RegisterView(CreateView):
    form_class =UserCreationForm
    success_url =reverse_lazy('accounts:login')
    template_name='accounts/register.html'


class LoginCustomView(LoginView):
    success_url =reverse_lazy('accounts:store')
    template_name='accounts/login.html'
