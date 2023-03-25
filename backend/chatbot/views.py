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
        print(request.body)
        data = json.loads(request.body.decode("utf-8"))
        disease_input=data['disease_input']
        num_days=data['num_days']
        print(disease_input,num_days)
        symp=get_symfromissue(disease_input,int(num_days))
        print(json.dumps(symp))
        return HttpResponse(json.dumps(symp))


@csrf_exempt
def get_res(request):
    if request.method=="POST":
        # print(request.POST.get('num_days'))
        data = json.loads(request.body.decode("utf-8"))
        symptoms_exp=data['symptoms_exp']
        num_days=data['num_days']
        present_disease=data['present_disease']
        res=get_result(symptoms_exp,int(num_days),present_disease)
        return HttpResponse(json.dumps(res))
