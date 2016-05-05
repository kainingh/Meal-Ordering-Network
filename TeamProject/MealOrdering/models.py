from __future__ import unicode_literals
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models
	
class Merchant(models.Model):
	"""
	this is the model for the Merchant
	@username, this username of this merchant
	@createTime, the time of this account creation
	@belonging, which user account this merchant is connected to 
	"""
	username = models.CharField(max_length = 100)
	createTime = models.DateTimeField(default = datetime.now, blank = True)
	belonging = models.ForeignKey(User)
	def __unicode__(self):
		return self.username

class Restaurant(models.Model):
	"""
	this is the model for Restaurant
	@name: the name of the restaurant 
	@description, the description of the restaurant
	@phoneNumber, the number of the restaurant
	@rating, the customers' rating of the restaurant
	@rateNumber, the whole number of ratings that the restaurant received
	@numberTotal, the total sell number of this restaurant
	@phtot, the photo of the restaurant
	@belonging, the owner of this restaurant
	@position, the position of the restaurant
	@createTime, the time that the owner create this restaurant
	"""
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 500)
	phoneNumber = models.DecimalField(max_digits = 20, decimal_places = 0)
	photo = models.ImageField(upload_to = "restaurant-photo", blank = True)
	belonging = models.ForeignKey(User)
	createTime = models.DateTimeField(default = datetime.now, blank = True)
	def __unicode__(self):
		return self.name

class RestaurantAddress(models.Model):
	"""
	this is the model for restaurant address
	@address, the specific address
	@city, city name
	@state, state name
	@zipcode, zipcode
	@belonging, this address belongs to which restaurant
	"""
	address = models.CharField(max_length = 200, blank = True)
	city = models.CharField(max_length = 200, blank = True)
	state = models.CharField(max_length = 200, blank = True)
	zipcode = models.DecimalField(max_digits = 5, decimal_places = 0, blank = True, default = 0)
	belonging = models.ForeignKey(Restaurant)
	def __unicode__(self):
		return address + '\n' + city + '\n' + state 
	
class Customer(models.Model):
	"""
	this is the model for Customer
	@username, the username of the customers
	@email, the email of the customer
	@belonging, which user account this customer is connected to 
	@favorRest, the favorite Restaurants of the customer
	@positon, the position of the customer
	@createTime, the creation time of this account
	"""
	username = models.CharField(max_length = 100)
	belonging = models.ForeignKey(User)
	createTime = models.DateTimeField(default = datetime.now, blank = True)
	photo = models.ImageField(upload_to = "customer-photo", blank = True)
	phoneNumber = models.CharField(max_length = 20, blank = True)
	def __unicode__(self):
		return self.username


class CustomerAddress(models.Model):
	"""
	this is the model for customer address
	@address, the specific address
	@city, city name
	@state, state name
	@zipcode, zipcode
	@belonging, this address belongs to which customer
	"""
	address = models.CharField(max_length = 200, blank = True)
	city = models.CharField(max_length = 30, blank = True)
	state = models.CharField(max_length = 30, blank = True)
	zipcode = models.CharField(max_length = 5, blank = True)
	belonging = models.ForeignKey(Customer)
	def __unicode__(self):
		return address + '\n' + city + '\n' + state 

class CreditCard(models.Model):
	"""
	this is the model for CreditCard
	@number, the number for the credit card
	@cvv, the cvv for the credit card
	@zipcode, the zipcode for the credit card
	@belonging, the credit card belong to which customer
	"""
	number = models.CharField(max_length = 20, blank = True)
	cvv = models.CharField(max_length = 3, blank = True)
	zipcode = models.CharField(max_length = 5, blank = True)
	expire = models.CharField(max_length = 5, blank = True)
	belonging = models.ForeignKey(Customer)
	def __unicode__(self):
		return self.number
	

class Dish(models.Model):
	"""
	this is the model for dish
	@name, the name of the dish
	@description, the description of the dish
	@price, the price of the dish
	@rating, customers' rating on this dish
	@rateNumber, the whole number of ratings that the restaurant received
	@numberTotal, the total sell number of this dish
	@photo, the photot of this dish
	@belonging, the restaurant which own this dish
	"""
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 400, blank = True)
	price = models.DecimalField(max_digits = 10, decimal_places = 2)
	numberTotoal = models.DecimalField(max_digits = 10, decimal_places = 0, default = 0, blank = True)
	belonging = models.ForeignKey(Restaurant)
	createTime = models.DateTimeField(default = datetime.now, blank = True)
	def __unicode__(self):
		return self.name 


class DishHistory(models.Model):
	"""
	this is the model for dish in history
	@dish, which dish is in pending
	@customer, which customer the pending dish belong to
	@number, the number of dish ordered
	@createTime, the dish create time
	"""
	dish = models.ForeignKey(Dish, related_name = 'history_dish')
	belonging = models.ForeignKey(Customer, related_name = 'history_customer')
	number = models.DecimalField(max_digits = 3, decimal_places = 1, default = 1)
	createTime = models.DateTimeField(default = datetime.now, blank = True)
	def __unicode__(self):
		return self.dish.name

class PendingOrder(models.Model):
	"""
	this is method to record a pending order in the restaurant page
	@wholemoney, the whole money in this order
	@creattime
	@dishes, all the dish ordered
	@belonging, this record belongs to which restaurant
	"""
	wholeMoney = models.DecimalField(max_digits = 10, decimal_places = 0, default = 0)
	createTime = models.DateTimeField(default = datetime.now, blank = True)		
	dishes = models.ManyToManyField(DishHistory)
	belonging = models.ForeignKey(Restaurant)

class HistoryOrder(models.Model):
	"""
	this is method to record history orders in the restaurant page
	@wholemoney, the whole money in this order
	@creattime
	@dishes, all the dish ordered
	@belonging, this record belongs to which restaurant
	"""
	wholeMoney = models.DecimalField(max_digits = 10, decimal_places = 0, default = 0)
	createTime = models.DateTimeField(default = datetime.now, blank = True)		
	dishes = models.ManyToManyField(DishHistory)
	belonging = models.ForeignKey(Restaurant)
	
class WholeOrder(models.Model):
	"""
	this is the method to record all the dish order request in one order
	@wholemoney, the whole money in this order
	@creattime
	@dishes, all the dish ordered
	@belonging, this record belongs to which customer
	"""
	restaurantName = models.CharField(max_length = 100)
	wholeMoney = models.DecimalField(max_digits = 10, decimal_places = 0, default = 0)
	createTime = models.DateTimeField(default = datetime.now, blank = True)		
	dishes = models.ManyToManyField(DishHistory)
	belonging = models.ForeignKey(Customer)
	

class DishUnpaid(models.Model):
	"""
	this is the model for dish in the basket
	@dish, which dish is in basket
	@customer, which customer the dish belongs to 
	@number, the number of the dish ordered
	@createTime, the dish order create time
	"""
	dish = models.ForeignKey(Dish, related_name = 'unpaid_dish')
	belonging = models.ForeignKey(Customer, related_name = 'unpaid_customer')
	number = models.DecimalField(max_digits = 3, decimal_places = 1, default = 1)
	createTime = models.DateTimeField(default = datetime.now, blank = True)
	def __unicode__(self):
		return self.dish.name
	
class CommentsOnRest(models.Model):
	"""
	this is the model for comments on restaurant
	@content, the comment's content
	@belonging, which restaurant this comment is comment on
	@commenter, this comment is comment by which customer
	@creatTime, the time that this comment is made
	"""
	content = models.CharField(max_length = 200)
	belonging = models.ForeignKey(Restaurant, related_name = 'comment_restaurant')
	commenter = models.ForeignKey(Customer, related_name = 'customer_comment_rest')
	createTime = models.DateTimeField(default = datetime.now, blank = True)
	def __unicode__(self):
		return self.content
		
class CommentsOnDish(models.Model):
	"""
	this is the model for comments on a dish
	@content, the comment's content
	@belonging, which dish this comment is comment on
	@commenter, this comment is comment by which customer
	@creatTime, the time that this comment is made
	"""
	content = models.CharField(max_length = 200)
	belonging = models.ForeignKey(Dish, related_name = 'comment_dish')
	commenter = models.ForeignKey(Customer, related_name = 'customer_comment_dish')
	createTime = models.DateTimeField(default = datetime.now, blank = True)
	def __unicode__(self):
		return self.content


