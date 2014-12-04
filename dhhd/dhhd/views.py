from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from plan.models import Plan, UserProfile
from plan.forms import UserForm

def index(request):
	# Query the database for a list of all the plans currently stored.
	# Order the plans by the number of likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in the context_dict dictionary which will be passed to the template engine.
	popular_plan_list = Plan.objects.order_by('-views')[:3]
	# Most recent plans
	recent_plan_list = Plan.objects.order_by('-pub_date')[:3]
	context_dict = {'popular_plans': popular_plan_list, 'recent_plans': recent_plan_list}
	return render(request, 'index.html', context_dict)
	
def about(request):
	return render(request, 'about.html', {})

"""
def register(request):
	# A boolean value for telling the template whether the registration was successful.
	# Set to False initially. Code changes value to True when registration succeeds.
	registered = False
	
	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
		# Attempt to grab information from the raw form information. 
		# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		###profile_form = UserProfileForm(data=request.POST)
		
		# If the form is valid
		if user_form.is_valid():
			# Save the user's data to the database
			user = user_form.save()
			
			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()
			
			# I think that this is how and when I need to create the new user profile, 
			# where the user will be able to store their favorite plans.
			profile = UserProfile(user=user)
			profile.save()
			
			registered = True
		
		# Invalid form - mistakes or something else. Print problems to terminal and to user
		else:
			print(user_form.errors)
			
	# Not a HTTP POST, so we render our form user using the ModelForm instance
	# The form will be ready blank and ready for user input.
	else:
		user_form = UserForm()
		
	# Render the template depending on the context
	return render(request,
		'register.html',
		{'user_form': user_form, 'registered': registered} )
		
def user_login(request):
	# if the request is a HTTP POST, try to pull out the relevant information
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		username = request.POST['username']
		password = request.POST['password']
		
		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)
		
		# If we have a user object, the details are correct.
		# If None, no user with matching credentials was found.
		if user:
			# Is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				# An inactive account was used - no logging in.
				return HttpResponse("Your account has been disabled for inactivity.")
		else:
			# Bad login details were provided. So we can't log the user in.
			print("Invalid login details: {}, {}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
	
	# The request is not a HTTP POST, so display the login form.
	# This scenario would most like be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence
		# the blank dictionary object.
		return render(request, 'login.html', {})
			
@login_required
def user_logout(request):
	# Since we know the user is already logged in, we can just log them out
	logout(request)
	return HttpResponseRedirect('/')
"""
	
@login_required
def myplans(request):
	return render(request, 'myplans.html', {})