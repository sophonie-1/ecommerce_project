from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.urls import reverse_lazy

from .models import *


class ProductListView(ListView):
    model=Product
    context_object_name ='products'
    template_name='store/product_list.html'
    ordering='-created_at'

class ProductDetailView(DetailView):
    model=Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'