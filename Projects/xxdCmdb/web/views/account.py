#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from repository import models
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from utils import ldap
from django.contrib.auth import authenticate, login

data_dict = {}


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        u1 = request.POST.get('username1', None)
        p1 = request.POST.get('pwd1', None)

        if u1 == 'admin':
            user = authenticate(username=u1, password=p1)
            if user is not None:
                if user.is_active:
                    print(user, type(user))
                    login(request, user)
                    print("User is valid, active and authenticated")

                    data_dict['status'] = True
                    data_dict['message'] = 'ok'

                    # 设置session
                    request.session['username'] = u1
                    request.session['is_login'] = True

                    ret = HttpResponse(json.dumps(data_dict))
                    ret.set_cookie('username', u1)
                    return ret
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                data_dict['status'] = False
                data_dict['message'] = '用户名或者密码错误...'
                return HttpResponse(json.dumps(data_dict))
        else:
            try:
                res, msg, email = ldap.authorize(user=u1, password=p1)

                # 域用户第一次登陆将会注册到userprofile
                if res:
                    user_nums = models.UserProfile.objects.filter(name=u1).count()
                    if user_nums < 1:
                        models.UserProfile.objects.create(name=u1)

                data_dict['status'] = True
                data_dict['message'] = 'ok'

                # 设置session
                request.session['username'] = u1
                request.session['is_login'] = True
                request.session.set_expiry(0)

                # django的用户认证
                # login(request, u1)

                ret = HttpResponse(json.dumps(data_dict))
                ret.set_cookie('username', u1)
                ret.set_cookie('email', email)
                return ret

            except Exception as e:
                print(e)
                data_dict['status'] = False
                data_dict['message'] = '用户名或者密码错误...'
                return HttpResponse(json.dumps(data_dict))


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        request.session.clear()
        return redirect('login.html')