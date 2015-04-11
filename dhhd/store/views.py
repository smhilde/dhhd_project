from __future__ import print_function

import re
import json
import pprint

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
			source = token,
			description = ', '.join([request.POST['customer_name'], 'Plan ' + request.POST['plan_number']]),
			statement_descriptor = 'Don Designs Plan ' + request.POST['plan_number'],
			receipt_email = request.POST['receipt_email'],
			metadata = {'email': request.POST['receipt_email'],
						'plan_number': request.POST['plan_number'],
						'shipping_method': 'Priority Ground',
						},
		)
	except stripe.error.CardError as e:
		# There was an error with the card
		body = e.json_body
		err = body.get('error')
		if err.get('code') in ('card_declined', 'card_expired'):
			err['message'] = err['message'] + ' Please try a different card.'
		elif err.get('code') in ('incorrect_cvc', 'incorrect_zip', 'address_zip_check', 'address_line1_check'):
			err['message'] = err['message'] + ' Please check the form and try again.'
		context_dict = {}
		context_dict['err'] = err
		form = CartForm(request.POST)
		context_dict['form'] = form
		plan_list = Plan.objects.get(number=request.POST['plan_number'])
		plan_list = plan.views.reformat_plan(plan_list)
		context_dict['plan_object'] = plan_list
		#print('Status is: {}'.format(e.http_status))
		#print('Type is: {}'.format(err.get('type')))
		#print('Code is: {}'.format(err.get('code')))
		#print('Params is: {}'.format(err.get('param')))
		#print('Message is: {}'.format(err.get('message')))
		return render(request, 'store/cart.html', context_dict)
	except stripe.error.InvalidRequestError as e:
		# Invalid parameters were supplied to Stripe's API
		body = e.json_body
		err = body.get('error')
		context_dict = {}
		context_dict['err'] = err
		form = CartForm(request.POST)
		context_dict['form'] = form
		plan_list = Plan.objects.get(number=request.POST['plan_number'])
		plan_list = plan.views.reformat_plan(plan_list)
		context_dict['plan_object'] = plan_list
		return render(request, 'store/cart.html', context_dict)
	except stripe.error.AuthenticationError as e:
		# Authentication with Stripe's API failed. Are the keys correct?
		body = e.json_body
		err = body.get('error')
		context_dict = {}
		context_dict['err'] = err
		form = CartForm(request.POST)
		context_dict['form'] = form
		plan_list = Plan.objects.get(number=request.POST['plan_number'])
		plan_list = plan.views.reformat_plan(plan_list)
		context_dict['plan_object'] = plan_list
		return render(request, 'store/cart.html', context_dict)
	except stripe.error.APIConnectionError as e:
		# Network communication with Stripe failed
		body = e.json_body
		err = body.get('error')
		context_dict = {}
		context_dict['err'] = err
		form = CartForm(request.POST)
		context_dict['form'] = form
		plan_list = Plan.objects.get(number=request.POST['plan_number'])
		plan_list = plan.views.reformat_plan(plan_list)
		context_dict['plan_object'] = plan_list
		return render(request, 'store/cart.html', context_dict)
	except stripe.error.StripeError as e:
		# Display a very generic error to the user, and maybe send yourself and email
		body = e.json_body
		err = body.get('error')
		context_dict = {}
		context_dict['err'] = err
		form = CartForm(request.POST)
		context_dict['form'] = form
		plan_list = Plan.objects.get(number=request.POST['plan_number'])
		plan_list = plan.views.reformat_plan(plan_list)
		context_dict['plan_object'] = plan_list
		return render(request, 'store/cart.html', context_dict)
	except Exception as e:
		# This covers all other exceptions. It might not be great to keep this exception.
		body = e.json_body
		err = body.get('error')
		context_dict = {}
		context_dict['err'] = err
		form = CartForm(request.POST)
		context_dict['form'] = form
		plan_list = Plan.objects.get(number=request.POST['plan_number'])
		plan_list = plan.views.reformat_plan(plan_list)
		context_dict['plan_object'] = plan_list
		return render(request, 'store/cart.html', context_dict)
	price = '${:.2f}'.format(float(charge.amount)/100)
	plan_object = Plan.objects.get(number=charge['metadata']['plan_number'])
	return render(request, 'store/checkout.html', {'charge': charge, 'plan_object': plan_object, 'price': price})

def terms(request):
	return render(request, 'store/terms.html', {})