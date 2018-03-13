#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import net
from web.service import ippool
from repository import models
from utils.response import BaseResponse
from web.service.login import auth_admin
from utils.menu import menu


@method_decorator(auth_admin, name='dispatch')
class NetListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(NetListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'net.html')


class NetJsonView(View):
    def get(self, request):
        obj = net.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = net.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = net.Asset.put_assets(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = net.Asset.post_assets(request)
        return JsonResponse(response.__dict__)


class IpListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(IpListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'ippool.html')


class IpJsonView(View):
    def get(self, request):
        obj = ippool.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = ippool.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = ippool.Asset.put_assets(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = ippool.Asset.post_assets(request)
        return JsonResponse(response.__dict__)

