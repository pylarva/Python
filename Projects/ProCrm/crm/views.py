from django.shortcuts import render
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def dashboard(request):
    """
    销售页面控制面板
    :param request:
    :return:
    """
    return render(request, 'crm/dashboard.html')


@login_required
def customers(request):
    """
    客户列表页面
    :param request:
    :return:
    """
    return render(request, 'crm/customers.html')
