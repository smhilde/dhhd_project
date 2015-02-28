from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from plan.models import Plan, SpecialFeature, UserProfile, User
from store.forms import CartForm
import re, stripe

stripe.api_key = "sk_test_MeEZRTb6IPCK7fd2Wf3YpOvQ"

def index(request):
	return redirect('/store/cart')

	
def cart(request):
	context_dict = {}
	
	if request.method == 'POST' and re.search('plan', request.META['HTTP_REFERER']): 
		plan_list = Plan.objects.get(number=request.POST['plan_number'])
		plan_list = reformat_plan(plan_list)
		context_dict['plan_object'] = plan_list

	elif request.method == 'POST':
		form = CartForm(request.POST)
		plan_list = Plan.objects.get(number=request.POST['plan_number'])
		plan_list = reformat_plan(plan_list)
		context_dict['plan_object'] = plan_list
		if form.is_valid():
			return checkout(request)
		else:
			context_dict['form'] = form
			return render(request, 'store/cart.html', context_dict)

	
	form = CartForm()	
	context_dict['form'] = form
	return render(request, 'store/cart.html', context_dict)

	
def checkout(request):
	# Get the credit card details submitted by the form
	token = request.POST['stripeToken']
	# Create the charge on Stripe's servers - this will charge the user's card.
	try:
		charge = stripe.Charge.create(
			amount = int(Plan.objects.get(number=request.POST['plan_number']).price * 100), # amount in cents
			currency = "usd",
			card = token,
			description = ', '.join([request.POST['customer_name'], 'Plan ' + request.POST['plan_number']]),
		)
	except stripe.CardError:
		# The card has been declined
		print('-------------- FAIL --------------')
		pass
		
	return render(request, 'store/checkout.html', {})

	
def reformat_plan(plan_list):
	try:
		for plan in plan_list:
			# Re-format the width and depth from floats to FF'-II" format.
			plan.width = str(int(plan.width)) + "'-" + str(round((plan.width - int(plan.width))*12)) + '"'
			plan.depth = str(int(plan.depth)) + "'-" + str(round((plan.depth - int(plan.depth))*12)) + '"'
			# Re-format bedrooms from float to int
			plan.bed = int(plan.bed)
			# Re-format price to string with format $XXXX.YY
			plan.price = '${:.2f}'.format(plan.price)
			# Re-format bathrooms to int if the number of bathrooms is whole
			if not plan.bath%1:
				plan.bath = int(plan.bath)
	except:
			# Re-format the width and depth from floats to FF'-II" format.
			plan_list.width = str(int(plan_list.width)) + "'-" + str(round((plan_list.width - int(plan_list.width))*12)) + '"'
			plan_list.depth = str(int(plan_list.depth)) + "'-" + str(round((plan_list.depth - int(plan_list.depth))*12)) + '"'
			# Re-format bedrooms from float to int
			plan_list.bed = int(plan_list.bed)
			# Re-format price to string with format $XXXX.YY
			plan_list.price = '${:.2f}'.format(plan_list.price)
			# Re-format bathrooms to int if the number of bathrooms is whole
			if not plan_list.bath%1:
				plan_list.bath = int(plan_list.bath)

	return plan_list
