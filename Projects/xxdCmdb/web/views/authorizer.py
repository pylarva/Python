#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import authorizer
from web.service.login import auth_admin


# @method_decorator(auth_admin, name='dispatch')
class AuthListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(AuthListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'auther_list.html')


class AuthJsonView(View):
    def get(self, request):
        obj = authorizer.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = authorizer.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = authorizer.Asset.put_assets(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = authorizer.Asset.post_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, device_type_id, asset_nid):
        response = authorizer.Asset.assets_detail(device_type_id, asset_nid)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class AddAssetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_asset.html')