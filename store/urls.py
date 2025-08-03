from django.urls import path
from .views import (ProductListView, ProductDetailView, 
                    CartView, AddToCartView, UpdateCartView,
                      RemoveFromCartView)



app_name = 'store'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/update/<int:item_id>/', UpdateCartView.as_view(), name='update_cart'),
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
]