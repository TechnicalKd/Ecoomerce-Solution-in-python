from django.shortcuts import render
from .forms import ProfieInfo,UserInfo
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from .models import Profile,User



# Create your views here.

def sign_up(request):
	form = UserInfo()

	if request.method == 'POST':
		form = UserInfo(request.POST)
		if form.is_valid():
			form.save()
			form = UserInfo(request.POST)
			return HttpResponseRedirect(reverse('App_login:user_login'))	
	return render(request,'App_login/signup.html',context={'form':form})


def user_login(request):
	form = AuthenticationForm()
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():	
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request,user)
				return HttpResponseRedirect(reverse('App_login:edit_profile'))													
	return render(request,'App_login/login.html',context={'form':form})



def edit_profile(request):
	profile = Profile.objects.get(user=request.user)

	form = ProfieInfo(instance=profile)

	if request.method == 'POST':
		form = ProfieInfo(request.POST,instance=profile)
		if form.is_valid():
			form = form.save()
			form = ProfieInfo(request.POST,instance=profile)

	return render(request,'App_login/edit_profile.html',context={'form':form})

def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('App_login:user_login'))	
