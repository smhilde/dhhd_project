from __future__ import print_function
import os
import re
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dhhd.settings')

import django
django.setup()

from django.utils import timezone
from plan.models import Plan, SpecialFeature, Customer

def populate(file_name):
	open_floor_plan = add_feature('bonus', 'Open Floor Plan')
	formal_dining = add_feature('bonus', 'Formal Dining')
	study = add_feature('bonus', 'Study')
	bonus_room = add_feature('bonus', 'Bonus Room')
	island_kitchen = add_feature('bonus', 'Island Kitchen')
	covered_patio = add_feature('bonus', 'Covered Patio')
	extra_living_room = add_feature('bonus', 'Extra Living Room')
	game_room = add_feature('bonus', 'Game Room')
	media_room = add_feature('bonus', 'Media Room')
	
	feature_dict = {
		'Open Floor Plan': open_floor_plan,
		'Formal Dining': formal_dining,
		'Study': study, 
		'Bonus Room': bonus_room, 
		'Island Kitchen': island_kitchen,
		'Covered Patio': covered_patio,
		'Living Room': extra_living_room,
		'Game Room': game_room,
		'Media Room': media_room,
	}

	address_pattern = re.compile('^(?P<number>\d+)\s(?P<street>[\w\s\.]+)')
	# distance_pattern = re.compile("^(?P<feet>\d+)\'-(?P<inches>\d+)\"")
	distance_pattern = re.compile("^(?P<feet>\d+)[\'\"\-=]+(?P<inches>\d+)")
	
	rendering_files = os.listdir('./plan/static/plan/')
	
	with open(file_name, newline='') as plan_data_file:
		planreader = csv.DictReader(plan_data_file)
		for plan in planreader:
			#w = validate_pattern(distance_pattern, plan['Width'])
			w = distance_pattern.search(plan['Width'])
			width = int(w.group('feet')) + float(w.group('inches'))/12
			
			#d = validate_pattern(distance_pattern, plan['Depth'])
			d = distance_pattern.search(plan['Depth'])
			depth = int(d.group('feet')) + float(d.group('inches'))/12
			
			features = []
			for key in feature_dict:
				if plan[key]:
					features.append(feature_dict[key])
			
			make_active = plan['Elevation File'] in rendering_files and plan['Floor Plan File'] in rendering_files
				
			add_plan(
				plan['Plan Number'],
				area=int(plan['Sq. Ft.']),
				bed=float(plan['Beds']),
				bath=float(plan['Baths']),
				floor=int(plan['Floors']),
				garage=int(plan['Garage']),
				living=int(plan['Living Areas']),
				width=width,
				depth=depth,
				price=plan['Price'],
				elevation_file=plan['Elevation File'],
				floorplan_file=plan['Floor Plan File'],
				planfeatures= features,
				active=make_active,
			)
				
	for feature in SpecialFeature.objects.all():
		print(feature)
	
	#for plan in Plan.objects.all():
	#	print(plan)
		
def add_plan(
		num, title=None, area=0, bed=2, bath=2.5, floor=1, garage=2, \
		living=1, width=None, depth=None, height=None, ceiling=9, price='ERR',  \
		pub_date=timezone.now(), views=0, likes=0, elevation_file='', \
		floorplan_file='', planfeatures=(), plancustomers=(), active=False):
		
	p = Plan.objects.get_or_create(
		number=num,
		title = title,
		area = area,
		bed = bed,
		bath = bath,
		floor = floor,
		garage = garage,
		living = living,
		width = width,
		depth = depth,
		height = height,
		ceiling = ceiling,
		price = price,
		pub_date = pub_date,
		views = views,
		likes = likes,
		elevation_file = elevation_file,
		floorplan_file = floorplan_file,
		active = active,
	)[0]
	p.save()
	for item in planfeatures:
		p.features.add(item)
	for item in plancustomers:
		p.customers.add(item)
	print(p)
	return p

def add_feature(room, feature):
	f = SpecialFeature.objects.get_or_create(room=room, feature=feature)[0]
	f.save()
	return f
	
def add_customer(name, acct_number):
	f = Customer.objects.get_or_create(name=name, acct_num=acct_number)[0]
	f.save()
	return f

def validate_pattern(pattern, string):
	res = pattern.search(string)
	if res is None:
		print('Did not validate string: {}'.format(string))
		new_string = input('Correct Input: ')
		if new_string:
			res = validate_pattern(pattern, new_string)
		else:
			raise Exception
	else:
		#print('Returning: {}'.format(res))
		return res
	
	

if __name__ == '__main__':
	print('Starting DHHD population script...')
	populate('../Plan Book Data 150310.csv')