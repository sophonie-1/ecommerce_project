from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    # list_filter = ['created_at']
    # date_hierarchy = 'created_at'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    list_filter = ['category', 'created_at', 'updated_at']
    list_editable = ['price', 'stock']
    date_hierarchy = 'created_at'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'created_at']
    search_fields = ['user__username', 'session_key']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    search_fields = ['cart__user__username', 'cart__session_key', 'product__name']
    list_filter = ['cart__created_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('cart__user', 'product')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'total_price', 'status', 'created_at']
    search_fields = ['user__username', 'session_key']
    list_filter = ['status', 'created_at']
    list_editable=['status']
    date_hierarchy = 'created_at'
    actions = ['mark_as_shipped']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f"{updated} order(s) marked as shipped.")
    mark_as_shipped.short_description = "Mark selected orders as shipped"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    search_fields = ['order__user__username', 'order__session_key', 'product__name']
    list_filter = ['order__created_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order__user', 'product')