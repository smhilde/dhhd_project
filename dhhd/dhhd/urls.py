from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.contrib import admin
from django.contrib.auth import views as auth_views
from registration.backends.simple.views import RegistrationView
from dhhd import views
#from plan import views as plan_views

class MyRegistrationView(RegistrationView):
	def get_success_url(self, request, user):
		return '/'

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^plan/', include('plan.urls'), name='plan'),
	#url(r'^plan\?=page', plan_views.index),
	#url(r'^register/', views.register, name='register'),
	#url(r'^login/', views.user_login, name='login'),
	#url(r'^logout/', views.user_logout, name='logout'),
	url(r'^myplans/', views.myplans, name='myplans'),
	url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
	#url(r'^accounts/password/reset/$', 
	#	auth_views.password_reset, 
	#	{'template_name': 'registration/password_reset.html',
	#	 'email_template_name': 'registration/password_reset_email.html',
	#	 'post_reset_redirect': reverse_lazy('auth_password_reset_done'),
	#	}, 
	#	name='auth_password_reset'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
)
