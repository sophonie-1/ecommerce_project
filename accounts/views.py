from django.shortcuts import render,redirect
from .models import *
from store.models import Cart,CartItem
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
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('store:product_list')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            # Merge guest cart with user cart
            session_key = self.request.session.session_key
            if session_key:
                guest_cart = Cart.objects.filter(session_key=session_key).first()
                if guest_cart:
                    user_cart, created = Cart.objects.get_or_create(user=user)
                    for guest_item in guest_cart.items.all():
                        user_item, created = CartItem.objects.get_or_create(
                            cart=user_cart,
                            product=guest_item.product
                        )
                        if not created:
                            user_item.quantity += guest_item.quantity
                        if user_item.quantity > user_item.product.stock:
                            messages.warning(
                                self.request,
                                f"Adjusted {user_item.product.name} to {user_item.product.stock} due to stock limits."
                            )
                            user_item.quantity = user_item.product.stock
                        if user_item.quantity > 0:
                            user_item.save()
                        else:
                            user_item.delete()
                    guest_cart.delete()
                    messages.info(self.request, "Your guest cart has been merged with your account.")
            messages.success(self.request, 'Logged in successfully!')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Invalid username or password.')
            return self.form_invalid(form)


class LogoutCustomView(View):
    def get(self,request):
        logout(self.request)
        messages.success(self.request,'Logged out successfully!')
        return redirect('store:product_list')