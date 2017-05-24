#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import release

USER_NAME = {}


def auth(func):
    def inner(request, *args, **kwargs):
        # v = request.COOKIES.get('user_cookie')
        v = request.session.get('is_login', None)
        if not v:
            return redirect('login.html')
        global USER_NAME
        USER_NAME['name'] = v
        return func(request, *args, **kwargs)
    return inner


# @method_decorator(auth, name='dispatch')
class ReleaseListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(ReleaseListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'release.html')


class ReleaseJsonView(View):
    def get(self, request):
        obj = release.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = release.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = release.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class ReleaseReadListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(ReleaseReadListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'release_r.html')