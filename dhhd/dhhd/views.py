from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("Welcome. This is the home page of Don Hildebrand Home Designs.")
