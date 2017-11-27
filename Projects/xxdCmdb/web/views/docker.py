#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
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
        data = models.DockerNode.objects.all()
        return render(request, 'dockers.html', {'data': data})

    def post(self, request):
        response = BaseResponse()

        # 操作容器
        is_handle = request.POST.get('is_handle')
        if is_handle:
            response = self.container_handle(request)
            return JsonResponse(response.__dict__)

        host_ip = request.POST.get('ip')
        response = self.container_inspect(host_ip)

        return JsonResponse(response.__dict__)

    def container_inspect(self, host_ip):
        """
        容器详细JSON
        :param host_ip:
        :return:
        """
        response = BaseResponse()

        c = docker.Client(base_url='tcp://%s:2375' % host_ip, version='auto', timeout=10)
        response.data = c.containers(quiet=False, all=True, trunc=True, latest=False, since=None,
                                     before=None, limit=-1)

        # ssh取每个容器的外网IP地址
        for i in response.data:
            i['Names'] = i['Names'][0].split('/')[1]

            cmd = "ssh root@%s docker exec %s ifconfig | awk 'NR==2 {print $2}'" % (host_ip, i['Names'])
            try:
                ret = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                i['NewIp'] = ret.stdout.read().strip()
            except Exception as e:
                i['NewIp'] = ''

        return response

    def container_handle(self, request):
        """
        操作容器
        :param request:
        :return:
        """
        ip = request.POST.get('ip')
        name = request.POST.get('name')
        cmd = request.POST.get('cmd')

        c = docker.Client(base_url='tcp://%s:2375' % ip, version='auto', timeout=10)

        if cmd == 'power':
            current_status = c.inspect_container(name).get('State').get('Status')
            print(c.inspect_container(name))
            if current_status == 'running':
                c.stop(name)
            else:
                c.start(name)
                # 根据容器名重新设置容器的IP地址
                old_ip = c.inspect_container(name).get('Config').get('Hostname').split('-')[-1]
                new_ip = '%s.%s' % ('.'.join(ip.split('.')[0:3]), old_ip)
                new_gateway = '%s.%s' % ('.'.join(ip.split('.')[0:3]), '253')
                cmd_shell = 'ssh root@%s pipework br0 %s %s/24@%s' % (ip, name, new_ip, new_gateway)
                try:
                    subprocess.Popen(cmd_shell, stdin=subprocess.PIPE, shell=True,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    time.sleep(2)
                except Exception as e:
                    print(e)

        if cmd == 'set_ip':
            cmd_shell = 'ssh root@%s '

        response = self.container_inspect(ip)
        return response



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
