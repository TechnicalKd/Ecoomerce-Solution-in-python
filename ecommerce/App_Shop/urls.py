from django.urls import path
from . import views

app_name = 'App_Shop'

urlpatterns = [

	path('',views.home.as_view(),name='home'),
	path('product-details<pk>',views.product_details.as_view(),name='product_details'),

]