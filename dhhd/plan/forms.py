from django import forms
from plan.models import Plan, SpecialFeature

class PlanForm(forms.Form):
	number = forms.IntegerField(label='Plan Number', required=False)
	min_area = forms.FloatField(label='Min Square Feet', initial=0, required=False)
	max_area = forms.FloatField(label='Max Square Feet', initial=20000, required=False)
	#min_bed = forms.FloatField(initial='Min Beds', required=False)
	#max_bed = forms.FloatField(initial='Max Beds', required=False)
	#min_bath = forms.FloatField(initial='Min Baths', required=False)
	#max_bath = forms.FloatField(initial='Max Baths', required=False)
	#floor = forms.FloatField(initial='# of Floors', required=False)
	#garage = forms.FloatField(initial='# Car Garage', required=False)
	#features = forms.ModelMultipleChoiceField(queryset=SpecialFeature.objects.all(), to_field_name='feature')