from django import forms
from plan.models import Plan, SpecialFeature, UserProfile
from django.contrib.auth.models import User
from django.forms import widgets
from registration.forms import RegistrationFormUniqueEmail, RegistrationFormTermsOfService
from django.utils.translation import ugettext_lazy as _

class PlanForm(forms.Form):
	number   = forms.CharField(label='Plan Number', required=False)
	min_area = forms.FloatField(label='Square Feet', required=False)
	max_area = forms.FloatField(label='Max Area', required=False)
	min_bed  = forms.FloatField(label='Bedrooms', required=False)
	max_bed  = forms.FloatField(label='Max Bedrooms', required=False)
	min_bath = forms.FloatField(label='Bathrooms', required=False)
	max_bath = forms.FloatField(label='Max Bathrooms', required=False)
	min_floor  = forms.FloatField(label='Floors', required=False)
	max_floor  = forms.FloatField(label='Max Floors', required=False)
	min_garage = forms.FloatField(label='Garages', required=False)
	max_garage = forms.FloatField(label='Max Garage', required=False)
	min_living = forms.FloatField(label='Living Areas', required=False)
	max_living = forms.FloatField(label='Max Living', required=False)
	min_width  = forms.CharField(label='House Width', required=False)
	max_width  = forms.CharField(label='', required=False)
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

class RegistrationFormDHHD(RegistrationFormUniqueEmail):
	"""
	Subclass of 'RegistrationFormUniqueEmail', which is a subclass of
	'RegistrationForm'. Adds fields for user's first and last names, not required.
	Overrides username, email, password1, and password2 to add a placeholder attribute
	in the HTML output.
	"""
	username = forms.RegexField(regex=r'^[\w.@+-]+$', max_length=30, label=_("Username"), 
								error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")},
								widget=forms.TextInput(attrs={'placeholder': 'Username'}))
	email = forms.EmailField(label=_("E-mail"), widget=forms.EmailInput(attrs={'placeholder': 'Email address'}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label=_("Password"))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password (again)'}), label=_("Password (again)"))

	first_name = forms.CharField(label=_('First Name'), required=False, widget=forms.TextInput(attrs={'placeholder': 'Your first name'}))
	last_name = forms.CharField(label=_('Last Name'), required=False, widget=forms.TextInput(attrs={'placeholder': 'Your last name'}))