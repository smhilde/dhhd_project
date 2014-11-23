from django.db import models
from django.utils import timezone

class Plan(models.Model):
	number = models.PositiveIntegerField('Plan Number', unique=True)
	title = models.CharField(max_length=1000, null=True, unique=True)
	area = models.PositiveIntegerField('Square Feet')
	bed = models.FloatField('Bedrooms')
	bath = models.FloatField('Bathrooms')
	floor = models.PositiveIntegerField('Number of Floors', default=1)
	garage = models.PositiveIntegerField('Garage Size')
	width = models.FloatField('House Width', null=True)
	depth = models.FloatField('House Depth', null=True)
	height = models.FloatField('House Height', null=True)
	ceiling = models.FloatField('Ceiling Height', null=True)
	price = models.FloatField('Plan Price', null=True)
	pub_date = models.DateTimeField('Date Published', default=timezone.now)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	features = models.ManyToManyField("SpecialFeature", null=True)
	customers = models.ManyToManyField("Customer", null=True)
	elevation_file = models.CharField('Elevation File', max_length=100)
	floorplan_file = models.CharField('Floor Plan File', max_length=100)
	
	def __str__(self):
		return '{}'.format(self.number)

class Customer(models.Model):
	name = models.CharField(max_length=100)
	acct_num = models.IntegerField('account number', unique=True)
	
	def __str__(self):
		return self.name

class User(models.Model):
	usrid = models.CharField(max_length=100, unique=True)
	usrpwd = models.CharField(max_length=100)
	plan = models.ManyToManyField(Plan)
	
	def __str__(self):
		return self.usrid

class Location(models.Model):
	street_number = models.IntegerField()
	street_name = models.CharField(max_length=250)
	town = models.CharField(max_length=250)
	state = models.CharField(max_length=250)
	zip_code = models.IntegerField()
	plan = models.ForeignKey(Plan)
	
	def __str__(self):
		return '{} {}, {}, {}  {}'.format(self.street_number, self.street_name, self.town, self.state, self.zip_code)

class SpecialFeature(models.Model):
	room = models.CharField(max_length=100)
	feature = models.CharField(max_length=100)
	
	def __str__(self):
		return '{}: {}'.format(self.room, self.feature)
