#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import vpn
from repository import models
from utils.response import BaseResponse
from web.service.login import auth_admin
from utils.menu import menu


@method_decorator(auth_admin, name='dispatch')
class VpnListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(VpnListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'vpn.html')


class VpnJsonView(View):
    def get(self, request):
        obj = vpn.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = vpn.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        obj = vpn.Asset()
        response = obj.put_assets(request)
        # response = vpn.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class AddVpnView(View):
    def get(self, request, *args, **kwargs):
        response = vpn.Asset.assets_info()
        return render(request, 'add_asset.html', {'response': response})

    def post(self, request):
        response = vpn.Asset.post_assets(request)
        return JsonResponse(response.__dict__)
