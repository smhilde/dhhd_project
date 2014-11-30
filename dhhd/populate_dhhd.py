import os
### Add print statements to populate() 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dhhd.settings')

import django
django.setup()

from django.utils import timezone
import csv, re
from plan.models import Plan, SpecialFeature, Customer

def populate():
	open_floor_plan   = add_feature('bonus', 'Open Floor Plan')
	formal_dining     = add_feature('bonus', 'Formal Dining')
	study             = add_feature('bonus', 'Study')
	bonus_room        = add_feature('bonus', 'Bonus Room')
	island_kitchen    = add_feature('bonus', 'Island Kitchen')
	covered_patio     = add_feature('bonus', 'Covered Patio')
	extra_living_room = add_feature('bonus', 'Extra Living Room')
	game_room         = add_feature('bonus', 'Game Room')
	media_room        = add_feature('bonus', 'Media Room')
	
	address_pattern = re.compile('^(?P<number>\d+)\s(?P<street>[\w\s\.]+)')
	distance_pattern = re.compile("^(?P<feet>\d+)\'-(?P<inches>\d+)\"")
	
	with open('../Plan Book Data.csv', newline='') as plan_data_file:
		planreader = csv.DictReader(plan_data_file)
		for plan in planreader:
			w = distance_pattern.search(plan['Width'])
			width = int(w.group('feet')) + float(w.group('inches'))/12
			
			d = distance_pattern.search(plan['Depth'])
			depth = int(d.group('feet')) + float(d.group('inches'))/12
			
			feature_dict = {'Open Floor Plan': open_floor_plan,
							'Formal Dining': formal_dining,
							'Study': study, 
							'Bonus Room': bonus_room, 
							'Island Kitchen': island_kitchen,
							'Covered Patio': covered_patio,
							'Living Room': extra_living_room,
							'Game Room': game_room,
							'Media Room': media_room,
			}
							
			features = []
			for key in feature_dict:
				if plan[key]:
					features.append(feature_dict[key])
			
			add_plan(
				plan['Plan Number'],
				area=int(plan['Sq. Ft.']),
				bed=float(plan['Beds']),
				bath=float(plan['Baths']),
				floor=int(plan['Floors']),
				garage=int(plan['Garage']),
				width=width,
				depth=depth,
				price=float(plan['Price']),
				elevation_file=plan['Elevation File'],
				floorplan_file=plan['Floor Plan File'],
				planfeatures= features,
			)
				
	for feature in SpecialFeature.objects.all():
		print(feature)
	
	for plan in Plan.objects.all():
		print(plan)
		
def add_plan(num, title=None, area=0, bed=2, bath=2.5, floor=1, garage=2, width=None, depth=None, height=None, ceiling=9, price=1000, pub_date=timezone.now(), views=0, likes=0, elevation_file='', floorplan_file='', planfeatures=(), plancustomers=()):
	p = Plan.objects.get_or_create(
		number=num,
		title = title,
		area = area,
		bed = bed,
		bath = bath,
		floor = floor,
		garage = garage,
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
	)[0]
	p.save()
	for item in planfeatures:
		p.features.add(item)
	for item in plancustomers:
		p.customers.add(item)
	return p

def add_feature(room, feature):
	f = SpecialFeature.objects.get_or_create(room=room, feature=feature)[0]
	f.save()
	return f
	
def add_customer(name, acct_number):
	f = Customer.objects.get_or_create(name=name, acct_num=acct_number)[0]
	f.save()
	return f

if __name__ == '__main__':
	print('Starting DHHD population script...')
	populate()