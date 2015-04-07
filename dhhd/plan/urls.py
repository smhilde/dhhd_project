from django.conf.urls import patterns, url
from plan import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='plan'),
	url(r'^(?P<plan_number>[\d\-A-Z]+)/$', views.details, name='details'),
	url(r'^like_plan/$', views.like_plan, name='like_plan'),
	)