# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import redirect
from django.shortcuts import render
from repository import models


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
        if user != 'admin':
            return redirect('read.html')
        if not v:
            return redirect('login.html')
        return func(request, *args, **kwargs)
    return inner


def auth_pm(func):
    def inner(request, *args, **kwargs):
        user = request.session['username']
        v = request.session.get('is_login', None)
        if not v:
            return redirect('login.html')
        group_obj = models.UserProfile.objects.filter(name=user).first()
        group_name = group_obj.group.name
        if group_name != 'pm':
            return render(request, 'read_list.html', {'response': '暂无PM审核权限..'})
        return func(request, *args, **kwargs)
    return inner


def auth_db(func):
    def inner(request, *args, **kwargs):
        user = request.session['username']
        v = request.session.get('is_login', None)
        if not v:
            return redirect('login.html')
        group_obj = models.UserProfile.objects.filter(name=user).first()
        group_name = group_obj.group.name
        if group_name != 'db':
            return render(request, 'read_list.html', {'response': '暂无DB审核权限..'})
        return func(request, *args, **kwargs)
    return inner


def auth_sa(func):
    def inner(request, *args, **kwargs):
        user = request.session['username']
        v = request.session.get('is_login', None)
        if not v:
            return redirect('login.html')
        group_obj = models.UserProfile.objects.filter(name=user).first()
        group_name = group_obj.group.name
        if group_name != 'sa':
            return render(request, 'read_list.html', {'response': '暂无SA审核权限..'})
        return func(request, *args, **kwargs)
    return inner
