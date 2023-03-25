from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_name, name='get_name'),
    path('symptoms', views.get_symptoms, name='get_symptoms'),
    path('results', views.get_res, name='get_res'),
]