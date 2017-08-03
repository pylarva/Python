#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import asset
from repository import models
from web.service.login import auth_admin

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


@method_decorator(auth_admin, name='dispatch')
class AssetListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(AssetListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'asset_list.html')


class AssetJsonView(View):
    def get(self, request):
        obj = asset.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = asset.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = asset.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, nid):
        asset_obj = models.Asset.objects.filter(id=nid).first()
        device_type_id = asset_obj.host_type
        response = asset.Asset.assets_detail(nid, device_type_id)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class AddAssetView(View):
    def get(self, request, *args, **kwargs):
        response = asset.Asset.assets_info()
        return render(request, 'add_asset.html', {'response': response})

    def post(self, request):
        response = asset.Asset.post_assets(request)
        return JsonResponse(response.__dict__)
