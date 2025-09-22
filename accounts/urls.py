from django.urls import path

from .views import RegisterView, LoginCustomView,LogoutCustomView,ProfileView,OrderCustumView


app_name ='accounts'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginCustomView.as_view(), name='login'),
    path('logout/', LogoutCustomView.as_view(), name='logout'),

    path('profile/',ProfileView.as_view(),name='profile'),
    path('user-s-orders/',OrderCustumView.as_view(),name='order_history')
]