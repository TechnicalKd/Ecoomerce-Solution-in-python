from django.urls import path
from . import views

app_name = 'App_login'


urlpatterns = [

	path('signup',views.sign_up,name='sign_up'),
	path('user_login',views.user_login,name='user_login'),
	path('edit_profile',views.edit_profile,name='edit_profile'),
	path('user_logout/',views.user_logout,name='user_logout'),
	
]