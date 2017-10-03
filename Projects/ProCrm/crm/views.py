from django.shortcuts import render
from django.conf.urls import url
from django.contrib import admin

# Create your views here.


def dashboard(request):

    return render(request, 'crm/base.html')
