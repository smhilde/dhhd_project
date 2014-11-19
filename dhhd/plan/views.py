from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("Plans says HELLO WORLD!. Find about all <a href='/plan/about'>about</a> us.")
	
def about(request):
	return HttpResponse("Don says, 'Here is the about page.' You can go back to <a href='/plan'>plans</a>, or return <a href='/'>home</a>.")
