from django.shortcuts import render
from django.http import HttpResponse

from plan.models import Plan

def index(request):
	# Query the database for a list of all the plans currently stored.
	# Order the plans by the number of likes in descending order.
	# Retrieve the top 5 only - or all if less than 5.
	# Place the list in the context_dict dictionary which will be passed to the template engine.
	popular_plan_list = Plan.objects.order_by('-likes')[:5]
	# Most recent plans
	recent_plan_list = Plan.objects.order_by('-pub_date')[:5]
	context_dict = {'popular_plans': popular_plan_list, 'recent_plans': recent_plan_list}
	return render(request, 'index.html', context_dict)
	
def about(request):
	context_dict = {'about_message': 'Don Hildebrand Home Designs, L.L.C., was established in September, 1995. With over thirty years of experience, Don possesses a wonderful sense of style and creativity. He is known for utilizing space and giving the home buyer all the amenities they request within the constraints of the home. Don has a support staff committed to creating a quality product. Our company works as a team to achieve these goals. We strive to stay abreast of the changing times, styles, wants, and needs of our customers. The goal of our company is to turn your dreams into a reality; a home you will be proud of for many years to come.'
		}
	return render(request, 'about.html', context_dict)
