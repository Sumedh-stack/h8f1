from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from asgiref.sync import async_to_sync
from chatbot.model.chat_bot import get_symfromissue, get_result

# Create your views here.
@csrf_exempt
def get_name(request):
    if request.method=="POST":
        name=request.POST['name']
        return HttpResponse("Hello, "+str(name))

@csrf_exempt
def get_symptoms(request):
    if request.method=="POST":
        disease_input=request.POST.get('disease_input')
        num_days=request.POST.get('num_days')
        # print(disease_input,num_days)
        symp=get_symfromissue(disease_input,num_days)
        return HttpResponse(json.dumps(symp))


@csrf_exempt
def get_res(request):
    if request.method=="POST":
        # print(request.POST.get('num_days'))
        symptoms_exp=request.POST.get('symptoms_exp')
        num_days=request.POST.get('num_days')
        present_disease=request.POST.get('present_disease')
        symptoms_exp=symptoms_exp[2:-2].split('", "')
        present_disease=present_disease[2:-2].split('", "')
        print(type(symptoms_exp))
    
        print(present_disease)
        res=get_result(symptoms_exp,num_days,present_disease)
        return HttpResponse(json.dumps(res))
