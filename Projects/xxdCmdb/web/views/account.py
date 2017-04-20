#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from repository import models
from django.shortcuts import render
from django.shortcuts import HttpResponse

data_dict = {}


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        u1 = request.POST.get('username1', None)
        p1 = request.POST.get('pwd1', None)

        if u1 or p1:

            user_num = models.AdminInfo.objects.filter(username=u1, password=p1).count()

            if user_num > 0:
                print(u1, p1, user_num)
                data_dict['status'] = True
                data_dict['message'] = 'ok'

                # 设置session
                request.session['username'] = u1
                request.session['is_login'] = True

                return HttpResponse(json.dumps(data_dict))

            else:
                data_dict['status'] = False
                data_dict['message'] = '用户名或者密码错误...'
                return HttpResponse(json.dumps(data_dict))


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        pass