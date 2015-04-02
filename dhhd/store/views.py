import re

from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import stripe

from plan.models import Plan, SpecialFeature, UserProfile, User
from store.forms import CartForm
import plan.views

stripe.api_key = "sk_test_MeEZRTb6IPCK7fd2Wf3YpOvQ"

def index(request):
	return redirect('/store/cart')

	
def cart(request):
	context_dict = {}
	
	if request.method == 'POST' and re.search('plan', request.META['HTTP_REFERER']): 
		plan_list = Plan.objects.get(number=request.POST['plan_number'])
		plan_list = plan.views.reformat_plan(plan_list)
		context_dict['plan_object'] = plan_list

	elif request.method == 'POST':
		form = CartForm(request.POST)
		plan_list = Plan.objects.get(number=request.POST['plan_number'])
		plan_list = plan.views.reformat_plan(plan_list)
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
	# Get the price of the plan in cents
	charge_price = int(plan.views.get_price(Plan.objects.get(number=request.POST['plan_number']).price)*100)
	# Create the charge on Stripe's servers - this will charge the user's card.
	try:
		charge = stripe.Charge.create(
			amount = charge_price, # amount in cents
			currency = "usd",
			card = token,
			description = ', '.join([request.POST['customer_name'], 'Plan ' + request.POST['plan_number']]),
		)
	except stripe.error.CardError as e:
		body = e.json_body
		err = body.get('error')
		# The card has been declined
		context_dict = {}
		form = CartForm(request.POST)
		context_dict['form'] = form
		plan_list = Plan.objects.get(number=request.POST['plan_number'])
		plan_list = plan.views.reformat_plan(plan_list)
		context_dict['plan_object'] = plan_list
		print('Status is: {}'.format(e.http_status))
		print('Type is: {}'.format(err.get('type')))
		print('Code is: {}'.format(err.get('code')))
		print('Params is: {}'.format(err.get('param')))
		print('Message is: {}'.format(err.get('message')))
		return render(request, 'store/cart.html', context_dict)
		
	return render(request, 'store/checkout.html', {})

