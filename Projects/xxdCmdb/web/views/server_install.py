#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import server
from web.service import ippool
from repository import models
from utils.response import BaseResponse
from web.service.login import auth_admin
from utils.menu import menu


@method_decorator(auth_admin, name='dispatch')
class ServerListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(ServerListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'server_install.html')

    def post(self, request, *args, **kwargs):

        # 前端新添加装机任务 检查是否允许装机 再添加装机任务
        response = BaseResponse()
        response.status = True
        ilo_ip = request.POST.get("ilo_ip")
        asset_id = request.POST.get('asset_id')
        if ilo_ip:
            server_obj = models.DellServer.objects.filter(manage_ip=ilo_ip).first()
            host_ip = models.Asset.objects.filter(id=asset_id).first().host_ip
            if server_obj.physical_server_status != 2:
                response.status = False
                response.message = '物理机已被安装系统或者为故障机'
            else:
                try:
                    # 装机任务所需的装机参数传给PhysicsInstall表
                    sn = server_obj.sn
                    hostname = server_obj.hostname
                    raid_level = server_obj.raid
                    ilo_ip = ilo_ip
                    server_model = server_obj.model
                    os_version = server_obj.os

                    # 查交换机
                    switch_obj = models.NIC.objects.filter(server_obj_id=server_obj.id).first()
                    switch_ip = switch_obj.switch_ip
                    switch_interface = switch_obj.switch_port

                    # 查vlan
                    vlan_obj = models.IpPool.objects.filter(ip=host_ip).first()
                    vlan = vlan_obj.vlan
                    gateway = vlan_obj.gateway

                    # 添加装机任务
                    models.PhysicsInstall.objects.create(sn=sn, ip=host_ip, hostname=hostname, raid_level=raid_level,
                                                         switch_ip=switch_ip, switch_interface=switch_interface,
                                                         ilo_ip=ilo_ip, server_model=server_model, os_version=os_version,
                                                         vlan=vlan, netmask='24', gateway=gateway, status=1)
                except Exception as e:
                    response.status = False
                    response.message = e

                response.message = '添加装机任务成功！'

        return JsonResponse(response.__dict__)


class ServerJsonView(View):
    def get(self, request):
        obj = server.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = server.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = server.Asset.put_assets(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = server.Asset.post_assets(request)
        return JsonResponse(response.__dict__)


