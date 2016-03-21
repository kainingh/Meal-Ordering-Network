from __future__ import unicode_literals
from django.contrib.auth.models import User
from datatime import datetime
from django.db import models

class Merchant(models.Model):
	"""
	this is the model for the Merchant
	@username, this username of this merchant
	@createTime, the time of this account creation
	"""
	username = models.CharField(max_length = 100)
	createTime = models.DateTimeField(default = datetime.now, blank = True)
	def __unicode__(self):
		return self.username

class Position(models.Model):
	"""
	this is the model for the an address and its position
	@address, the address name of the positon
	@coordinateX, @coordinateY the coordination of the position
	"""
	address = models.CharField(max_length = 200)
	coordinateX = models.DecimalField(max_digits = 3, decimal_places = 0)
	coordinateY = models.DecimalField(max_digits = 3, decimal_places = 0)
	def __unicode__(self):
		return address
	
class Restaurant(models.Model):
	"""
	this is the model for Restaurant
	@name: the name of the restaurant 
	@phoneNumber: the number of the restaurant
	@rating, the customers' rating of the restaurant
	@belonging, the owner of this restaurant
	@position, the position of the restaurant
	@createTime, the time that the owner create this restaurant
	"""
	name = models.CharField(max_length = 100)
	phoneNumber = models.CharField(max_length = 20)
	rating = models.DecimalField(max_digits = 3, decimal_places = 1, default = 0, blank = True)
	belonging = models.ForeignKey(Merchant, related_name = 'merchant_restaurant')
	position = models.ForeignKey(Position, realted_name = 'restaurant_position')
	createTime = models.DateTimeField(default = datetime.now, blank = True)
	def __unicode__(self):
		return self.name
		
class Customer(models.Model):
	"""
	this is the model for Customer
	@username, the username of the customers
	@email, the email of the customer
	@favorRest, the favorite Restaurants of the customer
	@positon, the position of the customer
	@createTime, the creation time of this account
	"""
	username = models.CharField(max_length = 100)
	email = models.EmailField(max_length = 100)
	favorRest = models.ManyToManyField(Restaurant)
	position = models.ForeignKey(Position, blank = True)
	createTime = models.DateTimeField(default = datetime.now, blank = True)
	def __unicode__(self):
		return self.username

class Dish(models.Model):
	"""
	this is the model for dish
	@name, the name of the dish
	@price, the price of the dish
	@rating, customers' rating on this dish
	@belonging, the restaurant which own this dish
	"""
	name = models.CharField(max_length = 100)
	price = models.DecimalField(max_digits = 5, decimal_places = 2)
	rating = models.DecimalField(max_digits = 3, decimal_places = 1, default = 0, blank = True)
	belonging = models.ForeignKey(Restaurant)
	createTime = models.DateTimeField(default = datetime.now, blank = True)
	def __unicode__(self):
		return self.name 
		
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
	commenter = models.ForeignKey(Customer, related_name = 'customer_comment')
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
	belonging = models.ForeignKey(dish, related_name = 'comment_dish')
	commenter = models.ForeignKey(Customer, related_name = 'customer_comment')
	createTime = models.DateTimeField(default = datetime.now, blank = True)
	def __unicode__(self):
		return self.content