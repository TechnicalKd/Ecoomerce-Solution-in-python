from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product,Category


# Create your views here.
class home(ListView):
	model = Product
	template_name = 'App_Shop/home.html'


class product_details(DetailView):
	model = Product
	template_name = 'App_Shop/product_details.html'
