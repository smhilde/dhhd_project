from django.contrib import admin
from plan.models import Plan, Customer, User, Location, SpecialFeature

class LocationInline(admin.TabularInline):
	model = Location
	extra = 1

class FeatureInline(admin.TabularInline):
	model = Plan.features.through

class CustomerInline(admin.TabularInline):
	model = Plan.customers.through

class PlanAdmin(admin.ModelAdmin):
	
	fieldsets = [
		(None, 			      {'fields': [('number', 'title'), 'area', ('bed', 'bath'), ('floor', 'garage', 'ceiling'), 'price']}),
		('Rendering Details', {'fields': [('elevation_file', 'floorplan_file')]}),
		('Footprint Details', {'fields': [('width', 'depth', 'height')], 'classes': ('collapse')}),
		('Date Information',  {'fields': ['pub_date'], 'classes': ('collapse')}),
		('Social Tracking',   {'fields': [('views', 'likes')], 'classes': ('collapse')}),
	]
	
	#filter_vertical = ('feature', 'customer')
	inlines = [
		LocationInline,
		FeatureInline,
		CustomerInline,
	]
	exclude = ('features', 'customers')
	list_display = ('number', 'area', 'bed', 'bath')
	list_filter = ['pub_date']
	search_fields = ['number']
	
admin.site.register(Plan, PlanAdmin)
admin.site.register(SpecialFeature)
admin.site.register(Customer)
admin.site.register(User)
