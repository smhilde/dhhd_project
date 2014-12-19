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
	elev_src = img_path + '1565_250.jpg'
	plan_src = img_path + '1742layout.jpg'
	for plan in Plan.objects.all():
		shutil.copyfile(elev_src, img_path + plan.number + '_elev.jpg')
		shutil.copystat(elev_src, img_path + plan.number + '_elev.jpg')
		
		shutil.copyfile(plan_src, img_path + plan.number + '_flrplan.jpg')
		shutil.copystat(plan_src, img_path + plan.number + '_flrplan.jpg')
		
		print('Copied images for plan {}'.format(plan.number))

if __name__ == '__main__':
	print('Starting create_temp_image script...')
	create_img()