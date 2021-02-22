from django.shortcuts import render
from django.http import HttpResponse
from .models import Events



# Create your views here.
def homepage(request):
    context = {
        'events': Events.objects.all()
    }
    return render(request,'Events/index.html', context)