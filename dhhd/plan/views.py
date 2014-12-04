from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from endless_pagination.decorators import page_template
from plan.models import Plan, SpecialFeature, UserProfile
from plan.forms import PlanForm, UserForm, UserProfileForm

def index(request):
	if request.method == 'POST':
		form = PlanForm(request.POST)
		if form.is_valid():
			plan_list = Plan.objects.all()
			if form.cleaned_data.get('number'):
				plan_list = Plan.objects.filter(number__exact=form.cleaned_data['number'])
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
			if form.cleaned_data.get('floor'):
				plan_list = plan_list.filter(floor__exact=form.cleaned_data['floor'])
			if form.cleaned_data.get('garage'):
				plan_list = plan_list.filter(garage__exact=form.cleaned_data['garage'])
			if form.cleaned_data.get('features'):
				feature_filter = Q()
				for feature in form.cleaned_data['features']:
					feature_filter = feature_filter | Q(features__feature__contains=feature)
				plan_list = plan_list.filter(feature_filter).distinct()
				#plan_list = plan_list.filter(features__feature__in=form.cleaned_data['features']) # <-- This query is the intersection of the features, and I think that I want the union
					
			return render(request, 'plan/results.html', {'form': form, 'plan_list': plan_list})

	else:
		form = PlanForm()
	return render(request, 'plan/index.html', {'form': form})
	
def details(request, plan_number):

	#Create a context dict which will be passed to the template rendering engine
	context_dict = {}
	context_dict['plan_number'] = plan_number
	
	try:
		# Can I find a plan with the given number?
		# If we can't, the .get() method raises a DoesNotExist exception.
		# So the .get() method returns one model instance or raises an exception.
		plan = Plan.objects.get(number=plan_number)
		context_dict['plan_object'] = plan
		plan.views += 1
		plan.save()
		
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
	
def plan_index(request, template='plan/plan_index.html', page_template='plan/plan_index_page.html'):
	context = {
		'plans': Plan.objects.all(),
		'page_template': page_template,
	}
	if request.is_ajax():
		template = page_template
	return render_to_response(template, context, context_instance=RequestContext(request))