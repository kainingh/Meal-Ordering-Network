from django import forms
from django.contrib.auth.models import User
from .models import *


class MerchantForm(forms.ModelForm):
	#the modelform for the modl merchant
	class Meta:
		model = Merchant
		exclude = ('createTime',)
	def clean_username(self):
		#the validation of the username
		username = self.cleaned_data('username')
		if len(username) > 100:
			raise forms.ValidationError('the length of the username must less than 100')
		return username

class PositionForm(forms.ModelForm):
	#the modelform for the model position
	class Meta:
		model = Position
		exclude = ()
	def clean_address(self):
		#the validation of address
		address = self.cleaned_data.get('address')
		if len(address) > 200:
			raise forms.ValidationError('the length of the address must less than 200')
		return address
	def clean_coordinate(self):
		#the validation of coordinations
		coordinateX = self.cleaned_data.get('coordinateX')
		coordinateY = self.cleaned_data.get('coordinateY')
		if len(coordinateX) > 3 or len(coordinateY) > 3:
			raise forms.ValidationError('the length of coordination must less or equal 3')
		else:
			try:
				int(coordinateX)
				int(coordinateY)
			except ValueError:
				raise forms.ValidationError('coordination must be a number')
		return coordinateX + coordinateY
		
class RestaurantForm(forms.ModelForm):
	#the modelform for the model restaurant
	class Meta:
		model = Restaurant
		exclude = ('belonging', 'position', 'rating', 'createTime')
	def clean_name(self):
		#the validation of restaurant name
		name = self.cleaned_data.get('name')
		if len(name) > 100:
			raise forms.ValidationError('Restaurant name length must less than 100')
		return name
	def clean_phoneNumber(self):
		#the validation of the phone number
		phoneNumber = self.cleaned_data('phoneNumber')
		if len(phoneNumber) != 10 or len(phoneNumber) != 11:
			raise forms.ValidationError('the length of the phoneNumber is not legal')
		else:
			try:
				int(phoneNumber)
			except ValueError:
				raise forms.ValidationError('phone number must be a number')
		return phoneNumber
		
class CustomerForm(forms.ModelForm):
	#the modelform for the model customer
	class Meta:
		model = Customer
		exclude = ('favorRest', 'position', 'createTime')
	def clean_name(self):
		#the validation of customer name
		name = self.cleaned_data('name')
		if len(name) > 100:
			raise forms.ValidationError('the length of name must less than 100')
		return name
	def clean_email(self):
		#the validation of customer email
		email = self.cleaned_data('email')
		if len(email) > 100:
			raise forms.ValidationError('the length of the email must less than 100')
		return email
	
class DishForm(forms.ModelForm):
	#the modelform for the model dish
	class Meta:
		model = Dish
		exclude = ('rating', 'belonging', 'createTime')
	def clean_name(self):
		#the validation of dish name
		name = self.cleaned_data('name')
		if len(name) > 100:
			raise forms.ValidationError('the length of dish name must less than 100')
		return name
	def price(self):
		#the validation of the price
		price = self.cleaned_data('price')
		try:
			float(price)
		except ValueError:
			raise forms.ValidationError('price must be a number')
		if price > 10000:
			raise forms.ValidationError('please dont be so greedy')
		return price
		
class CommentsOnRestForm(forms.ModelForm):
	#the modelform for the comments on restaurant
	class Meta:
		model = CommentsOnRest
		exclude = ('belonging', 'commenter', 'createTime')
	def clean_content(self):
		#the validation of the comment content
		content = self.cleaned_data('content')
		if len(content) > 200:
			raise forms.ValidationError('the length of the comment content must less than 200')
		return content

class CommentsOnDishForm(forms.ModelForm):
	#the modelform for the comments on dish
	class Meta:
		model = CommentsOnDish
		exclude = ('belonging', 'commenter', 'createTime')
	def clean_content(self):
		#the validation of the comment content
		content = self.cleaned_data('content')
		if len(content) > 200:
			raise forms.ValidationError('the length of the comment content must less than 200')
		return content
		