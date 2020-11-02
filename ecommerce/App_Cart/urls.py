from django.urls import path
from . import views

app_name = 'App_Cart'

urlpatterns = [
	
path('add_to_cart/<pk>',views.add_to_cart,name='add_to_cart'),
path('view_Cart',views.view_Cart,name='view_cart'),
path('remove_from_cart<pk>',views.remove_from_cart,name='remove_from_cart'),
path('increase_cart/<pk>',views.increase_cart,name='increase_cart'),
path('descrease_cart/<pk>',views.descrease_cart,name='descrease_cart')	
]