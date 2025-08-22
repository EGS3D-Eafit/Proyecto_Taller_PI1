from django.shortcuts import render
from .models import New

def news(request):
    news_s = New.objects.all().order_by('-date')
    return render(request, 'news.html', {'news_s': news_s})

# Create your views here.
