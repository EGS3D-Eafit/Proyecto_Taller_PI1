from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html', {'name': 'David Ballesteros Jaimes'})

def about(request):
    return render(request, 'about.html', {'name': 'waos'})
# Create your views here.
