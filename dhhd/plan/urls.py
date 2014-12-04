from django.conf.urls import patterns, url
from plan import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='plan'),
	url(r'^(?P<plan_number>[\d-]+)/$', views.details, name='details'),
	url(r'^test', views.plan_index),
	)