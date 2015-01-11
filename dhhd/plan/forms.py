from django import forms
from plan.models import Plan, SpecialFeature, UserProfile
from django.contrib.auth.models import User
from django.forms import widgets

class PlanForm(forms.Form):
	number   = forms.IntegerField(label='Plan Number', required=False)
	min_area = forms.FloatField(label='Min Square Feet', required=False)
	max_area = forms.FloatField(label='Max Square Feet', required=False)
	min_bed  = forms.FloatField(label='Min Bedrooms', required=False)
	max_bed  = forms.FloatField(label='Max Bedrooms', required=False)
	min_bath = forms.FloatField(label='Min Bathrooms', required=False)
	max_bath = forms.FloatField(label='Max Bathrooms', required=False)
	min_floor  = forms.FloatField(label='Min Floors', required=False)
	max_floor  = forms.FloatField(label='Max Floors', required=False)
	min_garage = forms.FloatField(label='Min Garage', required=False)
	max_garage = forms.FloatField(label='Max Garage', required=False)
	features = forms.ModelMultipleChoiceField(queryset=SpecialFeature.objects.all(), required=False, widget=widgets.CheckboxSelectMultiple)
	
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('fav_plans',)