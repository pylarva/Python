#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import authorize
from web.service.login import auth_admin


@method_decorator(auth_admin, name='dispatch')
class AuthListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(AuthListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'auth_list.html')


class AuthJsonView(View):
    def get(self, request):
        obj = authorize.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = authorize.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = authorize.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, device_type_id, asset_nid):
        response = authorize.Asset.assets_detail(device_type_id, asset_nid)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class AddAssetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_asset.html')