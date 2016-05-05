from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^$', views.loginPage, name = 'login_page'),
	url(r'^login$', views.loginSelf,  name = 'login'),
	url(r'^logout$', views.logoutSelf, name = 'logout'),
	url(r'^search/', include('haystack.urls')),
	#url(r'^loginredirect/(?P<authen>\w+)$', views.loginRedirect, name = 'login_redirect'),
	url(r'^register$', views.register, name = 'register'),
	url(r'^confirm/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9A-Z\-]+)$', views.confirm, name = 'confirm'),
	url(r'^mainpage$', views.mainPage, name = 'main_page'),
	url(r'^merchant/profile$', views.merchantProfile, name = 'merchant_profile'),
	url(r'^merchant/restaurant/(?P<id>\d+)$', views.restaurantProfile, name = 'restaurant_profile'),
	url(r'^merchant/restaurant/getPhoto/(?P<id>\d+)$', views.getRestPhoto, name = 'get_restaurant_photo'),
	url(r'^merchant/restaurant/editRestaurant/(?P<id>\d+)$', views.editRestaurant, name = 'edit_Restaurant'),
	url(r'^merchant/restaurant/postdish$', views.postDish, name = 'post_dish'),
	url(r'^merchant/restaurant/deletedish/(?P<dishId>\d+)/(?P<restId>\d+)$', views.deleteDish, name = 'delete_dish'),
	url(r'^merchant/createrestaurant$', views.createRestaurant, name = 'create_restaurant'),
	url(r'^merchant/deleterestaurant/(?P<id>\d+)$', views.deleteRestaurant, name = 'delete_restaurant'),
	url(r'^customer/profile/(?P<showPart>\d+)$', views.customerProfile, name = 'customer_profile'),
	url(r'^customer/editprofile$', views.editCustomer, name = 'edit_customer'),
	url(r'^customer/editcustomeraddress$', views.editCustomerAddress, name = 'edit_customer_address'),
	url(r'^customer/getphoto$', views.getCustomerPhoto, name = 'get_customer_photo'),
	url(r'^customer/editcredit$', views.editCredit, name = 'edit_credit'),
	url(r'^customer/unpaidpage/(?P<restaurantId>\d+)$', views.unpaidPage, name = 'unpaid_page'),
	url(r'^customer/deleteunpaid/(?P<id>\d+)$', views.deleteUnpaid, name = 'delete_unpaid'),
	url(r'^customer/orderdish$', views.dishOrder, name = 'order_dish'),
	url(r'^customer/paymoney/(?P<restaurantId>\d+)$', views.payMoney, name = 'pay_money'),
	url(r'^customer/addInformation', views.addInformation, name = 'add_information'),
	url(r'^customer/restaurantpage/(?P<id>\d+)$', views.restaurantPage, name = 'restaurant_page'),
	url(r'^customer/restaurantlist$', views.restaurantList, name = 'restaurant_list'),
	url(r'^customer/orderhistory', views.orderHistory, name = 'order_history'),
	
]