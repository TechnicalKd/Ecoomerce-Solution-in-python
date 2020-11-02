from django import forms
from .models import User,Profile
from django.contrib.auth.forms import UserCreationForm


class ProfieInfo(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = ('user',)



class UserInfo(UserCreationForm):
	class Meta:
		model = User
		fields = ('email','password1','password2')

		

