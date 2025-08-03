from django.views.generic import ListView, View,DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Product, Cart, CartItem
from django.contrib.auth.models import User

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    ordering = ['-created_at']

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

class CartView(ListView):
    template_name = 'store/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
        else:
            session_key = self.request.session.session_key
            print('what:',self.request)
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart.items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            cart = Cart.objects.get(user=user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            cart = Cart.objects.get(session_key=session_key)
        context['cart_total'] = sum(item.product.price * item.quantity for item in cart.items.all())
        return context
    
class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if product.stock <= 0:
            messages.error(request, f"{product.name} is out of stock.")
            return redirect('store:product_detail', pk=product_id)
        user = request.user
        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if product.stock < cart_item.quantity + 1:
            messages.error(request, f"Only {product.stock} {product.name} available.")
            return redirect('store:product_detail', pk=product_id)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"{product.name} added to cart.")
        return redirect('store:cart')

class UpdateCartView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, f"{cart_item.product.name} removed from cart.")
        else:
            if quantity > cart_item.product.stock:
                messages.error(request, f"Only {cart_item.product.stock} {cart_item.product.name} available.")
                return redirect('store:cart')
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"Updated {cart_item.product.name} quantity.")
        return redirect('store:cart')
    
class RemoveFromCartView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f"{product_name} removed from cart.")
        return redirect('store:cart')