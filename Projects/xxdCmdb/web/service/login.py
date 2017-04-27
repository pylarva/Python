# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import redirect


def auth(func):
    def inner(request, *args, **kwargs):
        # user = request.COOKIES.get('username')
        v = request.session.get('is_login', None)
        if not v:
            return redirect('login.html')
        return func(request, *args, **kwargs)
    return inner


def auth_admin(func):
    def inner(request, *args, **kwargs):
        user = request.COOKIES.get('username')
        v = request.session.get('is_login', None)
        # print(v)
        if user != 'admin':
            return redirect('read.html')
        if not v:
            return redirect('login.html')
        return func(request, *args, **kwargs)
    return inner