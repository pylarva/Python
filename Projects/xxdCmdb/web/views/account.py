#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from repository import models
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from utils import ldap

data_dict = {}


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        u1 = request.POST.get('username1', None)
        p1 = request.POST.get('pwd1', None)

        if u1 == 'admin':
            user_num = models.AdminInfo.objects.filter(username=u1, password=p1).count()
            if user_num > 0:
                data_dict['status'] = True
                data_dict['message'] = 'ok'

                # 设置session
                request.session['username'] = u1
                request.session['is_login'] = True

                ret = HttpResponse(json.dumps(data_dict))
                ret.set_cookie('username', u1)
                return ret
            else:
                data_dict['status'] = False
                data_dict['message'] = '用户名或者密码错误...'
                return HttpResponse(json.dumps(data_dict))
        else:
            res, msg, email = ldap.authorize(user=u1, password=p1)
            if res:
                data_dict['status'] = True
                data_dict['message'] = 'ok'

                # 设置session
                request.session['username'] = u1
                request.session['is_login'] = True

                ret = HttpResponse(json.dumps(data_dict))
                ret.set_cookie('username', u1)

                return ret
            else:
                data_dict['status'] = False
                data_dict['message'] = '用户名或者密码错误...'
                return HttpResponse(json.dumps(data_dict))


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        request.session.clear()
        return redirect('login.html')