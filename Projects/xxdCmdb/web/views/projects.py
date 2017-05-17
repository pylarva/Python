#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from django.views import View
from repository import models
from django.shortcuts import render
from django.http import JsonResponse
from utils.response import BaseResponse
from web.service import project


class ProjectsListView(View):
    def get(self, request, *args, **kwargs):
        data_list = models.ProjectTask.objects.all()
        return render(request, 'project_list.html', {'data_list': data_list})


class ProjectsJsonView(View):
    def get(self, request):
        obj = project.Project()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = project.Project.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = project.Project.put_assets(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = project.Project.post_users(request)
        return JsonResponse(response.__dict__)


from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
import json


class LdapListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ldap_list.html')

    def post(self, request):
        data_dict = {}
        user_loggedin = 'Guest'
        errors_list = []
        name = request.POST.get('name')
        password = request.POST.get('pwd')
        print(name, password)
        user = authenticate(username=name, password=password)
        print('authuser', user)
        # if user is not None:
        #     auth_login(request, user)
        #     uu = request.user
        #     u = User.objects.get(username=uu)
        #     return HttpResponse("../check_dict")
        data_dict['status'] = True
        return HttpResponse(json.dumps(data_dict))


        # context = {'errors_list': errors_list, 'user_loggedin': user_loggedin}
        # return render(request, 'aptest/loginauth.html', context)