from django.shortcuts import render
from django.http import HttpResponse
from plan.models import Plan, SpecialFeature
from plan.forms import PlanForm

def index(request):
	if request.method == 'POST':
		form = PlanForm(request.POST)
		if form.is_valid():
			plan_list = Plan.objects.filter(area__range=(form.cleaned_data['min_area'], form.cleaned_data['max_area']))
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
		# If we can't, the .got() method raises a DoesNotExist execption.
		# So the .get() method returns one model instance or raises an exception.
		plan = Plan.objects.get(number=plan_number)
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

