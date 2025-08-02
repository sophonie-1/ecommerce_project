from django.shortcuts import render,redirect
from .models import *

from django.views.generic import CreateView,FormView
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.views import LoginView,LogoutView
from django.views import View
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.urls import reverse_lazy



class RegisterView(FormView):
    form_class =UserCreationForm
    success_url =reverse_lazy('accounts:login')
    template_name='accounts/register.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request,user)
        messages.success(self.request,'Registration successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'Correct that error bellow')
        return super().form_invalid(form)



class LoginCustomView(FormView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    success_url =reverse_lazy('store:product_list')
    template_name='accounts/login.html'

    def form_valid(self, form):
        username =form.cleaned_data.get('username')
        password =form.cleaned_data.get('password')
        user =authenticate(self.request,username=username,password=password)
        if user is not None:
            login(self.request,user)
            messages.success(self.request, 'Logged in successfully!')
        else:
            messages.error(self.request,'User does not exist!!!!')
            return self.form_invalid(form)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"Please correct that error bellow")
        return super().form_invalid(form)


class LogoutCustomView(View):
    def get(self,request):
        logout(self.request)
        messages.success(self.request,'Logged out successfully!')
        return redirect('store:product_list')