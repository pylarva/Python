#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from repository import models
from web.service.login import auth_admin
from web.service import user
from django.utils.decorators import method_decorator


@method_decorator(auth_admin, name='dispatch')
class UserListView(View):
    def get(self, request, *args, **kwargs):
        user_list = models.UserProfile.objects.all()
        group_list = models.UserGroup.objects.all()
        business_one_list = models.BusinessOne.objects.all()
        business_two_list = models.BusinessTwo.objects.all()
        business_three_list = models.BusinessThree.objects.all()
        return render(request, 'users_list.html', {'user_list': user_list, 'group_list': group_list,
                                                   'business_one_list': business_one_list, 'business_two_list': business_two_list,
                                                   'business_three_list': business_three_list})


class UserJsonView(View):
    def get(self, request):
        obj = user.User()
        response = obj.fetch_users(request)
        return JsonResponse(response.__dict__)
        # return render(request, 'users_list.html', {'user_list': response.data['data_list']})

    def delete(self, request):
        response = user.User.delete_users(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = user.User.put_users(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = user.User.post_users(request)
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