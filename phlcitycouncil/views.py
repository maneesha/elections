from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, main page.")

def phlcitycouncil(request):
    return HttpResponse("vistiing phlcitycouncil")

def about(request):
    return HttpResponse('the about page')