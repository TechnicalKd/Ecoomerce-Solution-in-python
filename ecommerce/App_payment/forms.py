from django import forms
from .models import BillingsAddress


class MyAddress(forms.ModelForm):
	class Meta:
		model = BillingsAddress
		fields = ('address','zipcode','city','country')

