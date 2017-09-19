#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from django.views import View
from repository import models
from django.shortcuts import render
from django.http import JsonResponse
from utils.response import BaseResponse
from web.service import group
from django.utils.decorators import method_decorator
from web.service.login import auth_admin


@method_decorator(auth_admin, name='dispatch')
class ProjectListView(View):
    def get(self, request, *args, **kwargs):
        release_type = models.ReleaseType.objects.all()
        business_one_list = models.BusinessOne.objects.all()
        business_two_list = models.BusinessTwo.objects.all()
        business_three_list = models.BusinessThree.objects.all()
        return render(request, 'project.html', {'release_type': release_type, 'business_one_list': business_one_list,
                                                'business_two_list': business_two_list, 'business_three_list': business_three_list})

    def post(self, request, *args, **kwargs):
        response = BaseResponse()
        release_env = request.POST.get('obj_env')
        release_type = request.POST.get('obj_type')
        jdk_version = request.POST.get('jdk_version')
        git_url = request.POST.get('git_url')
        pack_cmd = request.POST.get('pack_cmd')
        username = request.POST.get('user_name')
        static_type = request.POST.get('static_cover_type')
        port = request.POST.get('port', None)

        # 检查是否有重复项目
        count = models.ProjectTask.objects.filter(business_2_id=release_env).count()
        if count != 0:
            response.status = False
            response.message = '该项目已存在..'
            return JsonResponse(response.__dict__)

        try:
            project_obj = models.ProjectTask(business_2_id=release_env, project_type_id=release_type,
                                             jdk_version=jdk_version, git_url=git_url, release_user=username,
                                             pack_cmd=pack_cmd, static_type=static_type, git_branch=port)
            project_obj.save()
        except Exception as e:
            print(e)

        response.status = True
        return JsonResponse(response.__dict__)


class ProjectJsonView(View):
    def get(self, request):
        obj = group.Group()
        response = obj.fetch_users(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = group.Group.delete_users(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = group.Group.put_users(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = group.Group.post_users(request)
        return JsonResponse(response.__dict__)


from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
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