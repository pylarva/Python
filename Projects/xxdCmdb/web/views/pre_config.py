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
from utils.response import BaseResponse
from conf import jenkins_config
from utils.menu import menu
from web.service.login import auth_config
from utils import logger
from conf import config_config


user_list = ['admin', 'xuguohua', 'yanyunfei']


def auth_admin(func):
    def inner(request, *args, **kwargs):
        user = request.COOKIES.get('username')
        v = request.session.get('is_login', None)
        if user not in user_list:
            return redirect('read.html')
        if not v:
            return redirect('login.html')
        return func(request, *args, **kwargs)
    return inner


# @method_decorator(auth_admin, name='dispatch')
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
        return render(request, 'pre_config.html', {'business_two_list': business_two_list})

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


# @method_decorator(auth_config, name='dispatch')
class ConfigListView(View):
    """
    用户界面的--配置修改
    """
    def dispatch(self, request, *args, **kwargs):
        return super(ConfigListView, self).dispatch(request, *args, **kwargs)

    def load_path(self, config_path, json_data):
        """
        递归遍历配置文件夹 发送json数据给前台tree插件 生成目录树
        :param config_path:
        :param json_data:
        :return:
        """
        pathList = os.listdir(config_path)
        for i, item in enumerate(pathList):
            config_dict = {}

            config_dict['title'] = item
            config_dict['open'] = 'false'
            config_dict['field'] = os.path.join(config_path, item)
            config_dict['candidate'] = 'true'

            if os.path.isdir(os.path.join(config_path, item)):
                config_dict['children'] = []
                config_dict['children'] = self.load_path(os.path.join(config_path, item), config_dict['children'])

            json_data.append(config_dict)
        return json_data

    def get(self, request, *args, **kwargs):
        response = BaseResponse()
        # 由于读取的配置文件夹不在本地 所以要先同步过来
        local_path = '/opt/%s' % os.path.basename(config_config.config_path)
        if os.path.exists(local_path):
            cmd = 'rm -fr %s' % local_path
            print(cmd)
            os.system(cmd)
        try:
            cmd = 'scp -r root@%s:%s /opt/' % (config_config.config_in_host_ip, config_config.config_path)
            os.system(cmd)
        except Exception as e:
            response.status = False
            response.message = '读取配置文件%s:%s失败..%s' % (config_config.config_in_host_ip, config_config.config_path, e)
            return JsonResponse(response.__dict__)

        json_data = []
        config_localhost_path = '/opt/%s' % os.path.basename(config_config.config_path)

        json_data = self.load_path(config_localhost_path, json_data)
        response.data = json_data
        response.status = True
        return JsonResponse(response.__dict__)
        ret = {}

        file = request.GET.get('file', None)
        business_id = request.GET.get('business_id', None)
        print(file, business_id)
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

        ret['menu'] = menu(request)
        response.data = ret
        return render(request, 'configs.html', {'business_two_list': business_two_list, 'response': response})

    def post(self, request):
        """
        修改配置文件
        :param request:
        :return:
        """
        response = BaseResponse()

        # 读取配置文件
        check_file = request.POST.get('check_file', None)
        if check_file and os.path.isfile(check_file):
            try:
                with open(check_file, "r") as f:
                    response.data = f.read()
                f.close()
                response.status = True
            except Exception as e:
                with open(check_file, "r", encoding='gb2312') as f:
                    response.data = f.read()
                f.close()
                response.status = True
            return JsonResponse(response.__dict__)

        # 新增配置文件
        new_file = request.POST.get('new_file', None)
        add_path = request.POST.get('add_path', None)
        if new_file and add_path:
            if os.path.isfile(add_path):
                response.status = False
                response.message = '添加失败, 选择【目录】进行添加..'
                return JsonResponse(response.__dict__)

            file = '%s/%s' % (add_path, new_file)
            file_dir = os.path.dirname(file)
            if not os.path.exists(file_dir):
                os.system('mkdir -p %s' % file_dir)
            cmd = 'touch %s' % file
            os.system(cmd)

            # 更新完后 要将本地文件夹同步回原主机
            try:
                cmd = 'scp -r /opt/%s root@%s:%s' % (os.path.basename(config_config.config_path),
                                                     config_config.config_in_host_ip, config_config.config_back_path)
                print(cmd)
                os.system(cmd)
                response.status = True
            except Exception as e:
                response.status = False
                response.message = '保存并同步配置文件失败..%s' % e
            response.status = True

        # 修改配置文件
        file_name = request.POST.get('file_name', None)
        file_content = request.POST.get('file_content', None)

        if file_name and file_content:
            if os.path.exists(file_name):
                os.system('chmod 777 %s' % file_name)
                with open(file_name, "w+") as f:
                    f.write(file_content)
                f.close()
                # logger.Logger().log('%s change config %s' % (request.session['username'], file), True)

            # 更新完后 要将本地文件夹同步回原主机
            try:
                cmd = 'scp -r /opt/%s root@%s:%s' % (os.path.basename(config_config.config_path),
                                                     config_config.config_in_host_ip, config_config.config_back_path)
                os.system(cmd)
                print(cmd)
                response.status = True
            except Exception as e:
                response.status = False
                response.message = '保存并同步配置文件失败..%s' % e

        return JsonResponse(response.__dict__)

