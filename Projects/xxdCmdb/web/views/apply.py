#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import apply
from web.service.login import auth_admin


# @method_decorator(auth_admin, name='dispatch')
class ApplyListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(ApplyListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'apply.html')


class ApplyJsonView(View):
    def get(self, request):
        obj = apply.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = apply.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = apply.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class ReleaseReadListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(ReleaseReadListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'release_r.html')