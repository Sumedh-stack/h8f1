from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def info(request):
    if request.method=="POST":
        name=request.GET['name']
        return HttpResponse("Hello, "+str(name))