from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.contrib import admin
from django.contrib.auth import views as auth_views
from dhhd import views
from plan.models import UserProfile
#from plan import views as plan_views


urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^plan/', include('plan.urls'), name='plan'),
	url(r'^myplans/', views.myplans, name='myplans'),
	url(r'^accounts/register/$', views.MyRegistrationView.as_view(), name='registration_register'),
	#url(r'^accounts/password/reset/$', 
	#	auth_views.password_reset, 
	#	{'template_name': 'registration/password_reset.html',
	#	 'email_template_name': 'registration/password_reset_email.html',
	#	 'post_reset_redirect': reverse_lazy('auth_password_reset_done'),
	#	}, 
	#	name='auth_password_reset'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
)
