from django.conf.urls import patterns, url
from plan import views

urlpatterns = patterns('',
	url(r'^$', views.index2, name='plan'),
	url(r'^(?P<plan_number>[\d-]+)/$', views.details, name='details'),
	url(r'^test/$', views.plan_index),
	url(r'^like_plan/$', views.like_plan, name='like_plan'),
	)