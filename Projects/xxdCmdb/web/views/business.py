#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import asset
from web.service import read
from web.service import business1
from web.service import business2
from web.service import business3
from repository import models
from utils.response import BaseResponse
from web.service.login import auth_admin


@method_decorator(auth_admin, name='dispatch')
class Business1ListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(Business1ListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'business_1_list.html')

    def post(self, request, *args, **kwargs):
        pass
        # response = BaseResponse()
        # try:
        #     business1_name = request.POST.get('business1_name')
        #     print(business1_name)
        #     models.BusinessOne.objects.create(name=business1_name)
        #     response.message = '添加成功'
        # except Exception as e:
        #     response.status = False
        #     response.message = str(e)
        # return response


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

    def post(self, request):
        response = business1.Asset.post_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, device_type_id, asset_nid):
        response = asset.Asset.assets_detail(device_type_id, asset_nid)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class AddAssetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_asset.html')


@method_decorator(auth_admin, name='dispatch')
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

    def post(self, request):
        response = business2.Asset.post_assets(request)
        return JsonResponse(response.__dict__)


@method_decorator(auth_admin, name='dispatch')
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

    def post(self, request):
        response = business3.Asset.post_assets(request)
        return JsonResponse(response.__dict__)