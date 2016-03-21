from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def PostDish(request):
	#this is the method for merchant to post a new dish
	error = []
	if not 'post' in request.POST or not request.POST['dish']