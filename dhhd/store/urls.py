from django.conf.urls import patterns, url
from store import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='store'),
	url(r'^cart/$', views.cart, name='cart'),
	url(r'^checkout/$', views.checkout, name='checkout'),
)