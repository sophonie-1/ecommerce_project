from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import RegisterView, LoginCustomView


app_name ='accounts'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginCustomView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]