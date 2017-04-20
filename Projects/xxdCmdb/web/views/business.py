#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import asset
from web.service import read
from web.service import business1
from web.service import business2
from web.service import business3


def auth(func):
    def inner(request, *args, **kwargs):
        v = request.session.get('is_login', None)
        print(v)
        if not v:
            return redirect('login.html')
        global USER_NAME
        USER_NAME['name'] = v
        return func(request, *args, **kwargs)
    return inner


# @method_decorator(auth, name='dispatch')
class Business1ListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(Business1ListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'business_1_list.html')


class Business1JsonView(View):
    def get(self, request):
        obj = business1.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = business1.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = business1.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, device_type_id, asset_nid):
        response = asset.Asset.assets_detail(device_type_id, asset_nid)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class AddAssetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_asset.html')


class Business2ListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(Business2ListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'business_2_list.html')


class Business2JsonView(View):
    def get(self, request):
        obj = business2.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = business2.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = business2.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class Business3ListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(Business3ListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'business_3_list.html')


class Business3JsonView(View):
    def get(self, request):
        obj = business3.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = business3.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = business3.Asset.put_assets(request)
        return JsonResponse(response.__dict__)