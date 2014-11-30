from django.conf.urls import patterns, include, url
from django.contrib import admin
from dhhd import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^plan/', include('plan.urls'), name='plan'),
	url(r'^register/', views.register, name='register'),
	url(r'^login/', views.user_login, name='login'),
	url(r'^logout/', views.user_logout, name='logout'),
)
