#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import release
from repository import models
from django.shortcuts import HttpResponse
from utils.response import BaseResponse


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


class ReleaseLogJsonView(View):
    def get(self, request):
        # obj = release.Asset()
        # response = obj.fetch_assets(request)
        response = BaseResponse()

        ret = {}
        # 从audit_sa.html 页面发送过来的日志请求
        release_last_id = request.GET.get('release_last_id', None)
        if release_last_id:
            release_id = int(release_last_id)
            values = models.ReleaseLog.objects.filter(release_id=release_id).only('release_time', 'release_msg')
            result = map(lambda x: {'time': x.release_time, 'msg': "%s" % x.release_msg}, values)
            result = list(result)
            ret['data_list'] = result
            response.status = True
            response.data = ret
            # response.data = json.dumps(ret)
            return JsonResponse(response.__dict__)

        # release.html 页面发来的日志请求
        release_id = request.GET.get('release_id', None)
        if release_id:
            values = models.ReleaseLog.objects.filter(release_id=release_id).only('release_time', 'release_msg')
            result = map(lambda x: {'time': x.release_time, 'msg': "%s" % x.release_msg}, values)
            result = list(result)
            ret['data_list'] = result
            response.status = True
            response.data = ret
            return JsonResponse(response.__dict__)

        release_id = request.GET.get('id', None)
        if not release_id:
            response.status = False
            response.data = ret
            return JsonResponse(response.__dict__)

        # print(release_id)
        obj = models.ProjectTask.objects.filter(id=release_id).first()

        if obj.release_last_id == '-':
            response.status = False
            return JsonResponse(response.__dict__)

        else:
            release_id = int(obj.release_last_id)
            values = models.ReleaseLog.objects.filter(release_id=release_id).only('release_time', 'release_msg')
            result = map(lambda x: {'time': x.release_time, 'msg': "%s" % x.release_msg}, values)
            result = list(result)

            ret['data_list'] = result
            response.status = True
            response.data = ret
            # response.data = json.dumps(ret)
            return JsonResponse(response.__dict__)

    def delete(self, request):
        response = release.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = release.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, device_type_id, asset_nid):
        response = release.Asset.assets_detail(device_type_id, asset_nid)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class AddAssetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_asset.html')