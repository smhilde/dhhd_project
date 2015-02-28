from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

class CartForm(forms.Form):
	customer_name = forms.CharField(label=_("Name:"), required=True, widget=forms.TextInput(attrs={'placeholder': 'First and Last Name', 'class': 'required'}))
	address_line1 = forms.CharField(label=_("Address Line 1:"), required=True, widget=forms.TextInput(attrs={'placeholder': '100 Main St.', 'class': 'required'}))
	address_line2 = forms.CharField(label=_("Address Line 2:"), required=False, widget=forms.TextInput(attrs={'placeholder': 'Ste. 200 / Apt. 7'}))
	address_city  = forms.CharField(label=_("City:"), required=True, widget=forms.TextInput(attrs={'placeholder': '', 'class': 'required'}))
	address_state = forms.CharField(label=_("State:"), required=True, widget=forms.TextInput(attrs={'placeholder': '', 'class': 'required'}))
	address_zip   = forms.CharField(label=_("Zip/Postal Code:"), required=True, widget=forms.TextInput(attrs={'placeholder': '', 'class': 'required'}))
	address_country = forms.CharField(label=_("Country:"), required=False, widget=forms.TextInput(attrs={'placeholder': '', 'value': 'USA'}))
	receipt_email = forms.EmailField(label=_("Email (for receipt):"), required=True, widget=forms.EmailInput(attrs={'placeholder': 'you@your_domain.com', 'class': 'required'}))
	