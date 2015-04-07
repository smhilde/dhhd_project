import re

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.db.models import Q
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
#from endless_pagination.decorators import page_template

from plan.models import Plan, SpecialFeature, UserProfile, User
from plan.forms import PlanForm, UserForm, UserProfileForm
import plan.prices

def index(request):
	if request.GET:
		form = PlanForm(request.GET)
		plan_list = None
		if form.is_valid():
			distance_pattern = re.compile("(?P<feet>\d+)\D+(?P<inches>\d+)")
			plan_list = Plan.objects.filter(active=True)
			if form.cleaned_data.get('number'):
				plan_list = Plan.objects.filter(active=True).filter(number__exact=form.cleaned_data['number'])
				return render(request, 'plan/results.html', {'form': form, 'plan_list': plan_list})
			if form.cleaned_data.get('min_area'):
				plan_list = plan_list.filter(area__gte=form.cleaned_data['min_area'])
			if form.cleaned_data.get('max_area'):
				plan_list = plan_list.filter(area__lte=form.cleaned_data['max_area'])
			if form.cleaned_data.get('min_bed'):
				plan_list = plan_list.filter(bed__gte=form.cleaned_data['min_bed'])
			if form.cleaned_data.get('max_bed'):
				plan_list = plan_list.filter(bed__lte=form.cleaned_data['max_bed'])
			if form.cleaned_data.get('min_bath'):
				plan_list = plan_list.filter(bath__gte=form.cleaned_data['min_bath'])
			if form.cleaned_data.get('max_bath'):
				plan_list = plan_list.filter(bath__lte=form.cleaned_data['max_bath'])
			if form.cleaned_data.get('min_floor'):
				plan_list = plan_list.filter(floor__gte=form.cleaned_data['min_floor'])
			if form.cleaned_data.get('max_floor'):
				plan_list = plan_list.filter(floor__lte=form.cleaned_data['max_floor'])
			if form.cleaned_data.get('min_garage'):
				plan_list = plan_list.filter(garage__gte=form.cleaned_data['min_garage'])
			if form.cleaned_data.get('max_garage'):
				plan_list = plan_list.filter(garage__lte=form.cleaned_data['max_garage'])
			if form.cleaned_data.get('min_living'):
				plan_list = plan_list.filter(living__gte=form.cleaned_data['min_living'])
			if form.cleaned_data.get('max_living'):
				plan_list = plan_list.filter(living__lte=form.cleaned_data['max_living'])
			
			if form.cleaned_data.get('min_width'):
				try:
					try:
						wdth = float(form.cleaned_data['min_width'])
					except:
						try:
							w = distance_pattern.search(form.cleaned_data['min_width'])
							wdth = int(w.group('feet')) + float(w.group('inches'))/12
						except:
							w = re.search('(\d+)',form.cleaned_data['min_width'])
							wdth = float(w.group(0))
				except:
					wdth = 0
				plan_list = plan_list.filter(width__gte=wdth)
				
			if form.cleaned_data.get('max_width'):
				try:
					try:
						wdth = float(form.cleaned_data['max_width'])
					except:
						try:
							w = distance_pattern.search(form.cleaned_data['max_width'])
							wdth = int(w.group('feet')) + float(w.group('inches'))/12
						except:
							w = re.search('(\d+)',form.cleaned_data['min_width'])
							wdth = float(w.group(0))
				except:
					wdth = 1e6	
				plan_list = plan_list.filter(width__lte=wdth)
			
			if form.cleaned_data.get('features'):
				feature_filter = Q()
				for feature in form.cleaned_data['features']:
					feature_filter = feature_filter | Q(features__feature__contains=feature)
				plan_list = plan_list.filter(feature_filter).distinct()

			plan_list = reformat_plan(plan_list)
			plan_list = plan_list.order_by('area')
	else:
		plan_list = Plan.objects.filter(active=True).order_by('area')
		plan_list = reformat_plan(plan_list)
		form = PlanForm()
	return render(request, 'plan/results.html', {'form': form, 'plan_list': plan_list, 'feature_list': SpecialFeature.objects.all()})


def details(request, plan_number):
	#Create a context dict which will be passed to the template rendering engine
	context_dict = {}
	context_dict['plan_number'] = plan_number
	if request.user.is_authenticated():
		context_dict['user_name'] = request.user.get_username()
		user_name = context_dict['user_name']
		user = User.objects.get(username=user_name)
		profile = UserProfile.objects.get(user=user)
		plan_list = profile.fav_plans.all()
		context_dict['is_favorite'] = plan_number in [plan.number for plan in plan_list]

	try:
		# Can I find a plan with the given number?
		# If we can't, the .get() method raises a DoesNotExist exception.
		# So the .get() method returns one model instance or raises an exception.
		plan = Plan.objects.get(number=plan_number)
		plan.views += 1
		plan.save()

		plan = reformat_plan(plan)

		context_dict['plan_object'] = plan

		plan_features = []
		for feature in plan.features.all():
			plan_features.append(feature.feature)
			# if I wanted to group the features by room, I could change this to find
			# all of the rooms in the features, and then for every room extract the feature.
			# For now, I just want the features, as this seems to be more reasonable if the
			# number of features are small. The features will have to be more descriptive.
			# If I keep this set up, its probably best to change the SpecialFeature model.

		if plan_features:
			context_dict['plan_features'] = plan_features

	except Plan.DoesNotExist:
		pass

	return render(request, 'plan/details.html', context_dict)

"""
@page_template('plan/plan_index_page.html')
def plan_index(request, template='plan/plan_index.html', extra_context=None):
	context = {
		'plans': Plan.objects.all(),
	}
	if extra_context is not None:
		context.update(extra_context)
	return render_to_response(template, context, context_instance=RequestContext(request))
"""

"""
def plan_index(request, template='plan/plan_index.html', page_template='plan/plan_index_page.html'):
	context = {
		'plans': Plan.objects.all(),
		'page_template': page_template,
	}
	if request.is_ajax():
		template = page_template
	return render_to_response(template, context, context_instance=RequestContext(request))
"""

def reformat_plan(plan_list):
	try:
		for plan in plan_list:
			# Re-format the width and depth from floats to FF'-II" format.
			plan.width = str(int(plan.width)) + "'-" + str(round((plan.width - int(plan.width))*12)) + '"'
			plan.depth = str(int(plan.depth)) + "'-" + str(round((plan.depth - int(plan.depth))*12)) + '"'
			# Re-format bedrooms from float to int
			plan.bed = int(plan.bed)
			# Re-format price to string with format $XXXX.YY
			plan.price = '${:.2f}'.format(get_price(plan.price))
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
			plan_list.price = '${:.2f}'.format(get_price(plan_list.price))
			# Re-format bathrooms to int if the number of bathrooms is whole
			if not plan_list.bath%1:
				plan_list.bath = int(plan_list.bath)

	return plan_list

def get_price(price_code):
	return plan.prices.price.get(price_code)
	
@login_required
def like_plan(request):
	"""
	if request.user.is_authenticated():
		user_name = request.user.get_username()
		user = User.objects.get(username=user_name)
		profile = UserProfile.objects.get(user=user)
	"""

	user_name = None
	if request.method == 'GET':
		user_name = request.GET['user_name']
		user = User.objects.get(username=user_name)
		profile = UserProfile.objects.get(user=user)

	plan_id = None
	if request.method == 'GET':
		plan_id = request.GET['plan_id']

	if plan_id:
		plan = Plan.objects.get(number=plan_id)
		if plan:
			plan.likes += 1
			plan.save()
			profile.fav_plans.add(plan)

	return HttpResponse('Saved to Favorites')
