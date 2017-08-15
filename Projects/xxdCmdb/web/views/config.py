#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import asset
from repository import models
# from web.service.login import auth_admin
from utils.response import BaseResponse
from conf import jenkins_config

user_list = ['admin', 'xuguohua', 'yanyunfei']


def auth_admin(func):
    def inner(request, *args, **kwargs):
        user = request.COOKIES.get('username')
        v = request.session.get('is_login', None)
        # print(v)
        if user not in user_list:
            return redirect('read.html')
        if not v:
            return redirect('login.html')
        return func(request, *args, **kwargs)
    return inner


@method_decorator(auth_admin, name='dispatch')
class AssetListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(AssetListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = BaseResponse()
        file = request.GET.get('file', None)
        business_id = request.GET.get('business_id', None)
        if file and business_id:
            business_obj = models.BusinessTwo.objects.filter(id=business_id).first()
            business_name = business_obj.name
            file_path = '%sprod/%s/%s' % (jenkins_config.config_path, business_name, file)
            try:
                with open(file_path, "r") as f:
                    response.data = f.read()
                f.close()
                response.status = True
            except Exception as e:
                with open(file_path, "r", encoding='gb2312') as f:
                    response.data = f.read()
                f.close()
                response.status = True
            return JsonResponse(response.__dict__)

        business = request.GET.get('business', None)
        if business:
            business_obj = models.BusinessTwo.objects.filter(id=business).first()
            business_name = business_obj.name
            config_path = '%sprod/%s/' % (jenkins_config.config_path, business_name)
            if os.path.exists(config_path):
                files = os.listdir(config_path)
                response.data = files
                response.status = True
            else:
                response.status = False
            return JsonResponse(response.__dict__)

        business_two_list = models.BusinessTwo.objects.all()
        return render(request, 'config.html', {'business_two_list': business_two_list})

    def post(self, request):
        """
        修改配置文件
        :param request:
        :return:
        """
        response = BaseResponse()

        # 新增配置文件
        new_file = request.POST.get('new_file', None)
        if new_file:
                business_id = request.POST.get('business_id', None)
                business_obj = models.BusinessTwo.objects.filter(id=business_id).first()
                business_name = business_obj.name
                file = '%sprod/%s/%s' % (jenkins_config.config_path, business_name, new_file)
                file_dir = os.path.dirname(file)
                if not os.path.exists(file_dir):
                    os.system('mkdir -p %s' % file_dir)
                cmd = 'touch %s' % file
                os.system(cmd)
                response.status = True

        # 修改配置文件
        business_id = request.POST.get('business_id', None)
        file_name = request.POST.get('file_name', None)
        file_content = request.POST.get('file_content', None)

        if business_id and file_name and file_content:
            business_obj = models.BusinessTwo.objects.filter(id=business_id).first()
            business_name = business_obj.name
            file = '%sprod/%s/%s' % (jenkins_config.config_path, business_name, file_name)
            if os.path.isfile(file):
                os.system('chmod 777 %s' % file)
                with open(file, "w+") as f:
                    f.write(file_content)
                f.close()
                response.status = True

        return JsonResponse(response.__dict__)


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
