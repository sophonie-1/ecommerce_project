from django.urls import path

from .views import RegisterView, LoginCustomView,LogoutCustomView


app_name ='accounts'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginCustomView.as_view(), name='login'),
    path('logout/', LogoutCustomView.as_view(), name='logout'),
]