import os
### Add print statements to populate() 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dhhd.settings')

import django
django.setup()

from django.utils import timezone
from plan.models import Plan
import shutil

def create_img():
	img_path = 'plan/static/plan/'
	elev_src = img_path + '1118_elev.jpg'
	plan_src = img_path + '1118_flrplan.jpg'
	for plan in Plan.objects.all():
		shutil.copyfile(elev_src, img_path + plan.number + '_elevation.jpg')
		shutil.copystat(elev_src, img_path + plan.number + '_elevation.jpg')
		
		shutil.copyfile(plan_src, img_path + plan.number + '_floorplan.jpg')
		shutil.copystat(plan_src, img_path + plan.number + '_floorplan.jpg')
		
		print('Copied images for plan {}'.format(plan.number))

if __name__ == '__main__':
	print('Starting create_temp_image script...')
	create_img()