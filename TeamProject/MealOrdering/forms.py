from django import forms
from django.contrib.auth.models import User
from .models import *

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		exclude = ('belonging', 'createTime',)
		def clean_number(self):
			number = self.cleaned_data.get('phoneNumber')
			if not number.isdigit():
				 raise forms.ValidationError('the phone number is not a digit')
		
class RestaurantForm(forms.ModelForm):
	class Meta:
		model = Restaurant
		exclude = ('belonging', 'createTime',)
		widgets = {
			'bio' : forms.Textarea(),
		}
		def clean_number(self):
			number = self.cleaned_data.get('phoneNumber')
			if not number.isdigit():
				 raise forms.ValidationError('the phone number is not a digit')
		
		