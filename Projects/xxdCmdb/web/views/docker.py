#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import docker
import subprocess
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import asset
from repository import models
from utils.response import BaseResponse
from web.service.login import auth_admin
from utils.menu import menu
from utils.response import BaseResponse


@method_decorator(auth_admin, name='dispatch')
class DockerView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(DockerView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'docker_index.html')


class DockersView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(DockersView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'dockers.html')

    def post(self, request):
        response = BaseResponse()
        host = request.POST.get('ip')
        print(host)
        c = docker.Client(base_url='tcp://%s:2375' % host, version='auto', timeout=10)
        response.data = c.containers(quiet=False, all=True, trunc=True, latest=False, since=None,
                                     before=None, limit=-1)
        for i in response.data:
            i['Names'] = i['Names'][0].split('/')[1]
            cmd = "ssh root@%s docker exec %s ifconfig | awk 'NR==2 {print $2}'" % (host, i['Names'])
            try:
                # i['NewIp'] = os.popen("ssh root@%s docker exec %s ifconfig | awk 'NR==2 {print $2}'" % (host, i['Names'])).read().strip()
                ret = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                i['NewIp'] = ret.stdout.read()
            except Exception as e:
                i['NewIp'] = ''
            # ssh取每个容器的外网IP地址
        return JsonResponse(response.__dict__)


class DockerJsonView(View):
    def get(self, request):
        """
        前端请求docker物理节点
        :param request:
        :return:
        """
        response = BaseResponse()

        response.data = [{
                    "ip": '192.168.1.1',
                    "time": "2017-11-19"
                }, {
                    "ip": '192.168.1.2',
                    "time": "2017-11-20"
                }]
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = asset.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = BaseResponse()
        response.data = [{
                    "ip": '192.168.1.1',
                    "time": "2017-11-20"
                }, {
                    "ip": '192.168.1.2',
                    "time": "2017-11-20"
                }]
        print(request)
        # response = asset.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, nid):
        asset_obj = models.Asset.objects.filter(id=nid).first()
        device_type_id = asset_obj.host_type
        response = asset.Asset.assets_detail(nid, device_type_id)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class ReleaseDetailView(View):
    def get(self, request, nid):
        response = BaseResponse()
        asset_obj = models.ReleaseTask.objects.filter(id=nid).first()
        response.data = asset_obj
        # device_type_id = asset_obj.host_type
        # response = asset.Asset.assets_detail(nid, device_type_id)

        ret = {}
        values = models.AuditLog.objects.filter(audit_id=nid).only('audit_time', 'audit_msg')
        result = map(lambda x: {'time': x.audit_time, 'msg': "%s" % x.audit_msg}, values)
        result = list(result)

        ret['data_list'] = result
        ret['menu'] = menu(request)
        print(ret)
        response.status = True

        return render(request, 'release_detail.html', {'response': response, 'log': ret})


class AddAssetView(View):
    def get(self, request, *args, **kwargs):
        response = asset.Asset.assets_info()
        return render(request, 'add_asset.html', {'response': response})

    def post(self, request):
        response = asset.Asset.post_assets(request)
        return JsonResponse(response.__dict__)
