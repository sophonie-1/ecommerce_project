from django.views.generic import ListView, View,DetailView,FormView
from django.shortcuts import get_object_or_404, redirect,render
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Product, Cart, CartItem,Order,OrderItem
from django.contrib.auth import login
from accounts.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from .forms import CheckOutForm

class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    ordering = ['-created_at']

    def get_queryset(self):
        # Override to ensure we only get products that are in stock
        return Product.objects.filter(stock__gt=0)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'


class CartView(ListView):
    template_name = 'store/cart.html'
    context_object_name = 'cart_items'

    # This method retrieves the cart items for the authenticated user or session.
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
    
    # This method calculates the total price of the cart items and adds it to the context.
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
        # Check if the product is in stock
        if product.stock <= 0:
            messages.error(request, f"{product.name} is out of stock.")
            return redirect('store:product_detail', pk=product_id)
        user = request.user
        # Get or create a cart for the user or session
        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        # If the item already exists in the cart, increase the quantity
        # because we set 1 as default quantity
        if not created:
            # Check if adding one more exceeds stock
            if product.stock <= cart_item.quantity + 1:
                messages.error(request, f"Only {product.stock} {product.name} available.")
                return redirect('store:product_detail', pk=product_id)
            # Otherwise, increase the quantity
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

class CheckoutView(FormView):
    template_name = 'store/checkout.html'
    form_class = CheckOutForm
    success_url = reverse_lazy('store:order_confirmation')

    # This method initializes the form with the user profile's shipping address if available.
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    # This method retrieves the cart items and total price to display on the checkout page.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            cart = Cart.objects.get(user=user)
        else:
            session_key = self.request.session.session_key
            cart = Cart.objects.get(session_key=session_key)
        context['cart_items'] = cart.items.all()
        context['cart_total'] = sum(item.product.price * item.quantity for item in cart.items.all())
        return context
    
    # This method handles the form submission for checkout.
    # It checks if the user is authenticated and retrieves the cart items.
    # If the user is not authenticated, it creates a session key for the cart.
    # It validates the stock of each item before creating the order.
    def form_valid(self, form):
        user = self.request.user
        if user.is_authenticated:
            cart = Cart.objects.get(user=user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key
            cart = Cart.objects.get(session_key=session_key)

        # Check stock before creating order
        for item in cart.items.all():
            if item.quantity > item.product.stock:
                messages.error(self.request, f"Only {item.product.stock} {item.product.name} available.")
                return redirect('store:cart')

        # user who created account during Checkout or ordering as quest
        if form.cleaned_data['create_account'] and not user.is_authenticated:
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            Profile.objects.create(user=user, address=form.cleaned_data['shipping_address'])
            login(self.request, user)
            messages.success(self.request, 'Account created and logged in!')
            cart.session_key = None
            cart.user = user
            cart.save()
        
        # Create order with the user or session key
        order = Order.objects.create(
            user=user if user.is_authenticated else None,
            session_key=session_key if not user.is_authenticated else None,
            total_price=sum(item.product.price * item.quantity for item in cart.items.all()),
            shipping_address=form.cleaned_data['shipping_address'],
        )
        messages.success(self.request, 'Order placed successfully!')

        # Create order items and update product stock by reducing number of items ordered
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()
        cart.items.all().delete()
        self.request.session['order_id'] = order.id
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
    
    # This view checks if the cart is empty before proceeding to checkout.
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            cart = Cart.objects.filter(user=user).first()
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart = Cart.objects.filter(session_key=session_key).first()
        if not cart or not cart.items.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect('store:cart')
        return super().get(request, *args, **kwargs)
       
class OrderConfirmationView(View):
    template_name = 'store/order_confirmation.html'

    # This view displays the order confirmation page after a successful order.
    # It retrieves the order using the order_id stored in the session.
    def get(self, request):
        order_id = request.session.get('order_id')
        if not order_id:
            messages.error(request, 'No order found.')
            return redirect('store:product_list')
        order = get_object_or_404(Order, id=order_id)
        return self.render_to_response({'order': order})
    
    # This method renders the order confirmation template with the order context.
    # It uses the render function to return the response.
    def render_to_response(self, context, **response_kwargs):
        return render(self.request, self.template_name, context, **response_kwargs)