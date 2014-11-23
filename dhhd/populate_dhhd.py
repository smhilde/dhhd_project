import os
### Add print statements to populate() 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dhhd.settings')

import django
django.setup()

from django.utils import timezone

from plan.models import Plan, SpecialFeature, Customer

def populate():
	wine_cooler = add_feature('kitchen', 'wine cooler')
	game_room = add_feature('bonus', 'game room')
	detached_garage = add_feature('garage', 'detached garage')
	shop = add_feature('bonus', 'detached shop')
	studio = add_feature('bonus', 'artist studio')
	
	add_plan(9991, title='Alpha', area=1532, garage=2, ceiling=8, price=525,
		elevation_file='1565_250.jpg', floorplan_file='1765layout.jpg',
		planfeatures=(wine_cooler, game_room),
		)
	add_plan(9992, title='Bravo', area=2574, bed=3, garage=3, ceiling=8, price=750,
		elevation_file='1586_250.jpg', floorplan_file='1792layout.jpg',
		planfeatures=(game_room, detached_garage),
		)
	add_plan(9993, title='Charlie', area=3215, bed=4, bath=3.5, floor=2, garage=3, ceiling=9, price=1000,
		elevation_file='1708_250_grayscale.jpg', floorplan_file='1813layout.jpg',
		planfeatures=(detached_garage, shop),
		)
	add_plan(9994, title='Delta', area=6843, bed=6, bath=4, floor=2, garage=4, ceiling=10, price=2500,
		elevation_file='1742_250_grayscale.jpg', floorplan_file='1742layout.jpg',
		planfeatures=(shop, studio),
		)
	add_plan(9995, title='Echo', area=1784, garage=3, ceiling=8, price=850,
		elevation_file='1765_250_grayscale.jpg', floorplan_file='1765layout.jpg',
		planfeatures=(studio, wine_cooler),
		)

	for feature in SpecialFeature.objects.all():
		print(feature)
	
	for plan in Plan.objects.all():
		print(plan)
		
def add_plan(num, title='', area=0, bed=2, bath=2.5, floor=1, garage=2, width=None, depth=None, height=None, ceiling=9, price=1000, pub_date=timezone.now(), views=0, likes=0, elevation_file='', floorplan_file='', planfeatures=(), plancustomers=()):
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