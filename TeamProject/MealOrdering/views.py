from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.http import HttpResponse, Http404
from django.db import transaction
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from mimetypes import guess_type
from django.core.mail import send_mail
# Create your views here.
"""
methods list:
$postDish, the method use to post a new dish(user should be a merchant)

"""

"""
Merchant relevant Methods List

"""
@transaction.atomic
def register(request):
	context = {}
	if request.method == 'GET':
		return render(request, 'register.html', context)
	username = request.POST['username']
	password = request.POST['password1']
	authen = request.POST['authen']
	email = request.POST['email']
	if User.objects.filter(username = username):
		return HttpResponse("sorry, the username has been registed")
	new_user = User.objects.create_user(username = username,  
                                       password = password,
										email = email) 
	new_user.is_active = False
	new_user.save()
	
	token = default_token_generator.make_token(new_user)
	
	email_body = """
	Welcome to Hello Food, Please click the link below to verify
	you account and complete the registration
	http://%s%s
	""" % (request.get_host(),
			reverse('confirm', args=(new_user.username, token + "AAA" + authen + "AAA" + password)))
	
	send_mail(subject="verify your email address",
			  message=email_body,
			  from_email="kainingh@andrew.cmu.edu",
			  recipient_list=[new_user.email])
	
	context = {
		'email' : email,
	}
	return render(request, 'confirm.html', context)

def confirm(request, username, token):
	user = get_object_or_404(User, username = username)
	pieces = token.split("AAA")
	token = pieces[0]
	authen = pieces[1]
	password = pieces[2]
	if not default_token_generator.check_token(user, token):
		raise Http404
	user.is_active = True
	user.save()	
	user = get_object_or_404(User, username = username)
	auth = authenticate(username = username, password = password)
	login(request, auth)
	if authen == "merchant":
		new_merchant = Merchant(username = username,
								belonging = user)
		new_merchant.save()
		return redirect('merchant_profile')
	elif authen == "customer":
		new_customer = Customer(username = username,
								belonging = user)
		new_customer.save()
		creditCard = CreditCard(belonging = new_customer)
		address = CustomerAddress(belonging = new_customer)
		creditCard.save()
		address.save()
		return redirect('customer_profile', showPart = 0)

def loginPage(request):
	#this is the method to show the login page
	context = {}
	return render(request, 'login.html', context)
	
def loginSelf(request):
	#this is the method to login
	context = {}
	username = request.POST['username']
	password = request.POST['password']
	authen = request.POST['authen']
	user = authenticate(username = username, password = password)
	if user is not None:
		if user.is_active:
			login(request, user)
			if authen == "merchant":
				if Merchant.objects.filter(belonging = user):
					return redirect('merchant_profile')
				else:
					context['error1'] = "sorry, you are not a merchant"
					return render(request, 'login.html', context)
			elif authen == "customer":
				if Customer.objects.filter(belonging = user):
					return redirect('haystack_search')
				context['error2'] = "sorry, you are not a customer"
				return render(request, 'login.html', context)
	return HttpResponse('sorry, user is not exists')

def logoutSelf(reqeust):
	#this method is to logout a user and then redirect to the login page
	logout(reqeust)
	return redirect('login_page')

def mainPage(request):
	context = {}
	if request.GET('search_rest'):
		return render()
@login_required
def merchantProfile(request):
	#this is the method to show merchant main page
	context = {}
	merchant = get_object_or_404(Merchant, belonging = request.user)
	restaurants = Restaurant.objects.filter(belonging = request.user)
	form = RestaurantForm()
	context = {
		'merchant' : merchant,
		'restaurants' : restaurants,
		'form' : form,
	}
	return render(request, 'merchant.html', context)

@login_required
def createRestaurant(request):
	#this is the method for a merchant to create a new restaurant
	context = {}
	address = request.POST['address']
	city = request.POST['city']
	state = request.POST['state']
	zipcode = request.POST['zipcode']
	new_restaurant = Restaurant(belonging = request.user)
	restaurantForm = RestaurantForm(request.POST, request.FILES, instance = new_restaurant)
	if not restaurantForm.is_valid():
		error = "sorry, the information you provide is not complete, please refill again"
		merchant = get_object_or_404(Merchant, belonging = request.user)
		restaurants = Restaurant.objects.filter(belonging = request.user)
		context = {
			'merchant' : merchant,
			'restaurants' : restaurants,
			'form' : RestaurantForm(),
			'error' : error,
		}
		return render(request , 'merchant.html', context)
	restaurantForm.save()
	restaurantAddress = RestaurantAddress(belonging = new_restaurant,
										  address = address,
										  city = city,
										  state = state,
										  zipcode = zipcode)
	try:
		restaurantAddress.save()
	except:
		new_restaurant.delete()
		return HttpResponse("sorry, the address information your provide is not valid")
		
	return redirect('merchant_profile')



@login_required
def deleteRestaurant(request, id):
	if restValidation(id, request.user) == 0:
		return HttpResponse("sorry, you have no right to behave like this")
	restaurantId = id 
	get_object_or_404(Restaurant, pk = restaurantId).delete()
	return redirect('merchant_profile')
	

@login_required
def restaurantProfile(request, id):
	#this is the method to show restaurant main page
	if restValidation(id, request.user) == 0:
		return HttpResponse("sorry, you have no right to behave like this")
	context = {}
	restaurant = get_object_or_404(Restaurant, pk = id)
	dishes = Dish.objects.filter(belonging = restaurant)
	comments = CommentsOnRest.objects.filter(belonging = restaurant)
	address = get_object_or_404(RestaurantAddress, belonging = restaurant)
	form = RestaurantForm()
	context = {
		'dishes' : dishes,
		'restaurant' : restaurant,
		'comments' : comments,
		'address' : address,
	}
	return render(request, 'restaurant.html', context)

@login_required
def getRestPhoto(request, id):
	#this is the method to get a restaurant's photo
	restaurant = get_object_or_404(Restaurant, pk = id)
	if not restaurant.photo:
		raise Http404
	content_type = guess_type(restaurant.photo.name)
	return HttpResponse(restaurant.photo, content_type = content_type)
	
def editRestaurant(request, id):
	#this is the method to create or edit restaurant profile
	if restValidation(id, request.user) == 0:
		return HttpResponse("sorry, you have no right to behave like this")
	restaurant = Restaurant(pk = id)
	form = RestaurantForm(request.POST, request.FILES, instance = restaurant)
	if not form.is_valid():
		return HttpResponse("sorry, the restaurant information you provide is not valid")
	form.save()
	return redirect('merchant_profile')
	
@login_required
def postDish(request):
	#this is the method for merchant to post a new dish
	context = {}
	name = request.POST['name']
	description = request.POST['description']
	price = request.POST['price']
	try:
		price = float(price)
	except:
		return HttpResponse("sorry, the price you tape in is not correct")
	restaurant_id = request.POST['restaurant_id']
	if restValidation(restaurant_id, request.user) == 0:
		return HttpResponse("sorry, you have no right to behave like this")
	restaurant = get_object_or_404(Restaurant, pk = restaurant_id)
	try:
		new_dish = Dish.objects.create(name = name,
										description = description,
										price = str(price),
										belonging = restaurant)
	except:
		error = "Sorry, the dish information you provide is not correct"
		dishes = Dish.objects.filter(belonging = restaurant)
		comments = CommentsOnRest.objects.filter(belonging = restaurant)
		address = get_object_or_404(RestaurantAddress, belonging = restaurant)
		form = RestaurantForm()
		context = {
			'dishes' : dishes,
			'restaurant' : restaurant,
			'comments' : comments,
			'address' : address,
			'error' : error,
		}
		return render(request, 'restaurant.html', context)
	new_dish.save()
	return redirect('restaurant_profile', id = restaurant_id)
	
@login_required
def deleteDish(request, dishId, restId):
	#this is the method for a restaurant to delete a dish
	context = {}
	if restValidation(restId, request.user) == 0:
		return HttpResponse("sorry, you have no right to behave like this")
	dish = get_object_or_404(Dish, pk = dishId)
	dish.delete()
	restaurant = get_object_or_404(Restaurant, pk = restId)
	return redirect('restaurant_profile', id = restId)
	
@login_required
def pendingPage(request, id):
	#this is the method to show all the pending orders
	context = {}
	restaurant = get_object_or_404(Restaurant, pk = id)
	pendingOrders = PendingOrder.objects.filter(belonging = restaurant)
	context = {
		'pendingOrders' : pendingOrders,
	}
	return render(request, 'pendingPage.html', context)

@login_required
def historyPage(request, id):
	#this is the method to show all the history order in a restaurant
	context = {}
	restaurant = get_object_or_404(Restaurant, pk = id)
	historyOrders = HistoryOrder.Objects.filter(belonging = restaurant)
	context = {
		'historyOrders' : historyOrders,
	}
	return render(request, 'historyPage.html', context)
	
@login_required
def completeOrder(request, id):
	#this is the method to complete an order
	pendingOrder = get_object_or_404(PendingOrder, pk = id)
	restaurantId = pendingOrder.belonging.pk
	dishes = pendingOrder.dishes.all()
	historyOrder = HistoryOrder(wholeMoney = pendingOrder.wholeMoney,
								belonging = pendingOrder.belonging,
								dishes = pendingOrder.dishes.all())
	historyOrder.save()
	pendingOrder.delete()
	return redirect('')

def restValidation(restaurantId, user):
	restaurant = get_object_or_404(Restaurant, pk = restaurantId)
	restUser = restaurant.belonging
	if restUser == user:
		return 1;
	else:
		return 0;
"""
end of merchant relevant methods
"""




"""
Customer relevant methods
"""
@login_required
def addInformation(request):
	#this is the method for a customer to add information
	customer = get_object_or_404(Customer, belonging = request.user)
	customerForm = CustomerForm(request.POST, request.FILES, instance = customer)
	if not customerForm.is_valid():
		return HttpResponse("sorry, the customer information you provide is not valid")
	address = request.POST['address']
	city = request.POST['city']
	state = request.POST['state']
	zipcode = request.POST['zipcode']
	if not zipcode.isdigit():
		return HttpResponse("sorry, the customer address information you provide is not correct")
	customerAddress = get_object_or_404(CustomerAddress, belonging = customer)
	customerAddress.address = address
	customerAddress.city = city
	customerAddress.state = state
	customerAddress.zipcode = zipcode
	try:
		customerAddress.save()
	except:
		return HttpResponse("sorry, the customer address information you provide is not correct")
	zipcode1 = request.POST['zipcode1']
	expire = request.POST['expire']
	number = request.POST['number']
	cvv = request.POST['cvv']
	if not (cvv.isdigit() and number.isdigit() and zipcode1.isdigit()):
		return HttpResponse("sorry, the creditcard information you provide is not correct")
	creditCard = get_object_or_404(CreditCard, belonging = customer)
	creditCard.number = number
	creditCard.cvv = cvv
	creditCard.zipcode = zipcode1
	creditCard.expire = expire
	try:
		creditCard.save()
	except:
		return HttpResponse("sorry, the creditcard information you provide is not correct")
	return redirect('customer_profile', showPart = 0)
	
@login_required
def customerProfile(request, showPart):
	#this is the method to show the customer's profile
	context = {}
	customer = get_object_or_404(Customer, belonging = request.user)
	form = CustomerForm()
	wholeOrders = WholeOrder.objects.filter(belonging = customer)
	creditCard = get_object_or_404(CreditCard, belonging = customer)
	address = get_object_or_404(CustomerAddress, belonging = customer)
	context['customer'] = customer
	context['form'] = form
	context['wholeOrders'] = wholeOrders
	context['showPart'] = showPart
	context['address'] = address
	context['creditCard'] = creditCard
	return render(request, 'customer.html', context)

@login_required
def editCustomer(request):
	#this is the method to edit the customer's profile
	context = {}
	customer = get_object_or_404(Customer, belonging = request.user)
	customerForm = CustomerForm(request.POST, request.FILES, instance = customer)
	if not request.POST['phoneNumber'].isdigit():
		return HttpResponse("sorry, the customer information your provide is not valid")
	
	customerForm.save()
	form = CustomerForm()
	context['customer'] = customer
	context['form'] = form
	context['showPart'] = '0'
	return render(request, 'customer.html', context)
	
@login_required
def getCustomerPhoto(request):
	#this is the method to get a customer's photo
	customer = get_object_or_404(Customer, belonging = request.user)
	if not customer.photo:
		raise Http404
	content_type = guess_type(customer.photo.name)
	return HttpResponse(customer.photo, content_type = content_type)

@login_required
def editCredit(request):
	#this is the method use to edit the credit card information
	context = {}
	number = request.POST['number']
	cvv = request.POST['cvv']
	zipcode = request.POST['zipcode']
	expire = request.POST['expire']
	if not (cvv.isdigit() and number.isdigit() and zipcode.isdigit()):
		return HttpResponse("sorry, the creditcard information you provide is not correct")
	customer = get_object_or_404(Customer, belonging = request.user)
	form = CustomerForm()
	if CreditCard.objects.filter(belonging = customer):
		creditCard = CreditCard.objects.get(belonging = customer)
		creditCard.number = number
		creditCard.cvv = cvv
		creditCard.zipcode = zipcode
		creditCard.expire = expire
		try:
			creditCard.save()
		except:
			return HttpResponse("sorry, the credit card information you provide is not valid")
		return redirect('customer_profile', showPart = 2)
		#return HttpResponse('modified success')

	else:
		new_credit = CreditCard(belonging = customer,
								number = number,
								cvv = cvv,
								zipcode = zipcode,
								expire = expire)
		new_credit.save()
		return redirect('customer_profile', showPart = 2)
@login_required
def editCustomerAddress(request):
	#this is the method to edit the customer address
	context = {}
	customer = get_object_or_404(Customer, belonging = request.user)
	address = request.POST['address']
	city = request.POST['city']
	state = request.POST['state']
	zipcode = request.POST['zipcode']
	if not zipcode.isdigit():
		return HttpResponse("sorry, the address information your provide is not valid")
	if CustomerAddress.objects.filter(belonging = customer):
		customerAddress = CustomerAddress.objects.get(belonging = customer)
		customerAddress.address = address
		customerAddress.city = city
		customerAddress.state = state
		customerAddress.zipcode = zipcode
		try:
			customerAddress.save()
		except:
			return HttpResponse("sorry, the address information your provide is not valid")
		return redirect('customer_profile', showPart = 1)
	else:
		new_customerAddress = CustomerAddress(belonging = customer,
											  city = city,
											  state = state,
											  zipcode = zipcode)
		new_custoemrAddress.save()
		return redirect('customer_profile', showPart = 1)

@login_required
def restaurantList(request):
	#this is the page to show the restaurant list
	context = {}
	restaurants = Restaurant.objects.all()
	context = {
		'restaurants' : restaurants,
	}
	return render(request, 'restaurantList.html', context)
@login_required
def restaurantPage(request, id):
	#this is the method to show the restaurant page for user to order dish
	context = {}
	restaurant = get_object_or_404(Restaurant, pk = id)
	dishes = Dish.objects.filter(belonging = restaurant)
	customer = get_object_or_404(Customer, belonging = request.user)
	unpaidDishes = DishUnpaid.objects.filter(belonging = customer)
	context = {
		'restaurant':restaurant,
		'dishes' : dishes,
		'unpaidDishes' : unpaidDishes,
	}
	return render(request, 'restaurantPage.html', context)
@login_required
def dishOrder(request):
	#this is the method to order dish
	context = {}
	dishId = request.POST['dish_id']
	dish = get_object_or_404(Dish, pk = dishId)
	restaurantId = request.POST['restaurant_id']
	if DishUnpaid.objects.all():
		previousRest = DishUnpaid.objects.all()[0].dish.belonging.pk
		if str(previousRest) != restaurantId:
			return HttpResponse("sorry, you have only make order in one restaurant in one time")
	customer = get_object_or_404(Customer, belonging = request.user)
	number = request.POST['number']
	new_dishUnpaid = DishUnpaid(belonging = customer,
								number = number,
								dish = dish)
	try:
		number = int(number)
	except:
		context['error'] = "sorry, your order number is not valid"
		return HttpResponse("sorry, your order number is not valid")
	if number <= 0:
		return HttpResponse("sorry, the order number should be a positive number")
	new_dishUnpaid.save()
	return redirect('restaurant_page', id = restaurantId)

@login_required
def deleteUnpaid(request, id):
	#this is the method to cancel an unpaid order
	unpaidDish = get_object_or_404(DishUnpaid, pk = id)
	dish = unpaidDish.dish
	restaurant = dish.belonging
	unpaidDish.delete()
	return redirect('restaurant_page', id = restaurant.pk) 

@login_required
def unpaidPage(request, restaurantId):	
	#this is the method to show the list of unpaid dishes
	customer = get_object_or_404(Customer, belonging = request.user)
	dishes = DishUnpaid.objects.filter(belonging = customer)
	address = get_object_or_404(CustomerAddress, belonging = customer)
	creditCard = get_object_or_404(CreditCard, belonging = customer)
	wholeMoney = 0
	for dish in dishes:
		wholeMoney += dish.dish.price * dish.number
	context = {
		'dishes' : dishes,
		'address' : address,
		'creditCard':creditCard,
		'wholeMoney':wholeMoney,
		'customer':customer,
		'restaurantId':restaurantId,
	}
	return render(request, 'unpaidDishes.html', context)
	
@login_required
def payMoney(request, restaurantId):
	#this is the method for a customer to pay for the order
	context={}
	customer = get_object_or_404(Customer, belonging = request.user)
	unpaidDishes = DishUnpaid.objects.filter(belonging = customer)
	address = get_object_or_404(CustomerAddress, belonging = customer)
	creditCard = get_object_or_404(CreditCard, belonging = customer)
	restaurant = get_object_or_404(Restaurant, pk = restaurantId)
	permit = 1
	if not (address.address and address.city and address.state and address.zipcode):
		permit = 0
	if not (creditCard.number and creditCard.cvv and creditCard.zipcode  and creditCard.expire):
		permit = 0
	if unpaidDishes:
		if permit==0:
			form = CustomerForm()
			context['form']=form
			return render(request, 'infomation.html', context )
		else:
			wholeMoney = 0
			wholeOrder = WholeOrder(belonging = customer)
			wholeOrder.save()
			email = restaurant.belonging.email
			email_body = """
			Dear Chef:
				Your customer just place order:
			""" 
			email_body += "\n"
			for dish in unpaidDishes:
				new_dishHistory = DishHistory(dish = dish.dish,
											belonging = dish.belonging,
											number = dish.number)
				new_dishHistory.save()
				wholeMoney += dish.number * dish.dish.price
				wholeOrder.dishes.add(new_dishHistory)
				email_body += dish.dish.name + "\t"
				email_body += str(dish.number) + "\n"
				dish.delete()
			wholeOrder.wholeMoney = wholeMoney
			wholeOrder.restaurantName = restaurant.name
			wholeOrder.save()
			address = get_object_or_404(CustomerAddress, belonging = customer)
			email_body += "from customer" + "\t" + customer.username + "\n"
			email_body += "Address:" + "\n"; 
			email_body += address.address + "\n"
			email_body += "Phone Number:" + "\n";
			email_body += str(customer.phoneNumber)
			send_mail(subject="Order received",
					  message=email_body,
					  from_email="kainingh@andrew.cmu.edu",
					  recipient_list=[restaurant.belonging.email])
			return redirect('customer_profile', showPart = 3)
	return redirect('unpaid_page', restaurantId = restaurantId)
@login_required
def orderHistory(request):
	#this is the method to show the history order of a customer
	context = {}
	customer = get_object_or_404(Customer, belonging = request.user)
	historyDishes = DishHistory.objects.filter(belonging = customer)
	context = {
		'historyDishes' : historyDishes,
	}
	return render(request, 'dishHistory.html', context)
	
@login_required
def commentOnRest(request):
	#this is the method for the customer to comment on a restaurant
	context = {}
	comment = request.POST['comment']
	restaurantId = request.POST['restaurant_id']
	commenter = request.user
	restaurant = get_object_or_404(Restaurant, pk = restaurantId)
	new_comment = CommentOnRest(belonging = restaurant,
								commenter = commenter,
								content = comment)
	new_comment.save()
	return redirect('restaurant_page', id = restaurantId)
		
@login_required
def commentOnDish(request):
	#this is the method for the customer to comment on a dish
	errors = []
	
	if not 'comment' in request.POST or not request.POST['comment']:
		errors.append('You must enter a comment')
	else:
		content = request.POST['comment']
		dishId = request.POST['dishid']
		rating = request.POST['rating']
		try:
			dish = Dish.objects.get(pk = dishId)
			new_comment = CommentOnDish(content = content,
									 belonging = dish,
									 commenter = request.user)
			new_comment.save()
		except ObjectDoesNotExist:
			errors.append('No corresponding dish')
	if errors:
		return HttpResponse(errors)
	else:
		return HttpResponse('comment success')
		
@login_required
def rateOnDish(request):
	#this is the method for the customer to rate on a dish
	errors = []
	if not 'rating' in request.POST or not request.POST['rating']:
		errors.append('there must be a rating value')
	else:
		rating = request.POST['rating']
		try:
			#if the post rating is not a integer, post error message
			rating = int(rating)
			if rating < 0 or rating > 5:
				errors.append('the rating value must in range 0 ~ 5')
			else:
				# if there are no corresponding dish, post error message
				dishId = request.POST['dishId']
				try:
					dish = Dish.objects.get(pk = dishId)
					rateNumber = dish.rateNumber
					wholeRating = rateNumber * dish.rating + rating
					dish.rateNumber = rateNumber + 1
					dish.rating = wholeRating / (rateNumber + 1)
					dish.save()
				except ObjectDoesNotExist:
					errors.append('the corresponding dish dose not exist')
		except ValueError:
			errors.append('the rating value must an integer')
	
	if errors:
		return HttpResponse(errors)
	else:
		return HttpResponse('Make rate success')
		
		


