#!/usr/bin/env python
# -*- coding:utf-8 -*-
import paramiko
from conf import config_config
from django.db.models import Q
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
            # 资产状态有两个 一个是asset表里面 另一个是dellserver表里面
            # (1, '已装机'),
            # (2, '未装机'),
            # (3, '故障机'),
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
                    print('server_install.py', sn, hostname, ilo_ip)
                    response.message = '添加装机任务成功！'
                except Exception as e:
                    response.status = False
                    response.message = str(e)

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
        """
        开始执行装机任务
        :param request:
        :return:
        """
        # response = server.Asset.post_assets(request)
        response = BaseResponse()
        response.status = True

        # 装机日志
        ret = {}

        install_log_id = request.POST.get('install_log_id')
        if install_log_id:
            release_id = int(install_log_id)
            values = models.InstallLog.objects.filter(install_id=release_id).only('install_time', 'install_msg')
            result = map(lambda x: {'time': x.install_time, 'msg': "%s" % x.install_msg}, values)
            result = list(result)
            if not result:
                response.status = False
            ret['data_list'] = result
            response.data = ret

        install_id = request.POST.get('install_id')
        if install_id:

            # 开始执行安装
            models.InstallLog.objects.create(install_id=install_id, install_msg='开始安装系统...')
            try:
                models.PhysicsInstall.objects.filter(id=install_id).update(status=2)
                i_obj = models.PhysicsInstall.objects.filter(id=install_id).first()

                cmd = 'python {0} {1} {2} {3} {4} RAID{5} {6} {7} {8} ' \
                      '{9} {10} {11} {12} {13}'.format(config_config.install_scripts_path,
                                                       i_obj.id, i_obj.sn, i_obj.ip,
                                                       i_obj.hostname, i_obj.raid_level,
                                                       i_obj.switch_ip, i_obj.switch_interface,
                                                       i_obj.ilo_ip, i_obj.server_model,
                                                       i_obj.os_version, i_obj.vlan,
                                                       '255.255.255.0', i_obj.gateway)
                print(cmd)
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(config_config.install_scripts_ip, port=22, username='root', password='xinxindai318', timeout=3)
                ssh.exec_command(cmd)
                models.InstallLog.objects.create(install_id=install_id, install_msg=config_config.install_scripts_ip)
                models.InstallLog.objects.create(install_id=install_id, install_msg=cmd)
            except Exception as e:
                print(e)
                response.message = str(e)
                response.status = False

        # 前端页面请求任务状态
        task_id = request.POST.getlist('install_task_id', None)
        if task_id:
            task_id_list = task_id
            con_q = Q()
            con_q.connector = 'OR'
            for item in task_id_list:
                con_q.children.append(('id', item))
            obj_list = models.PhysicsInstall.objects.filter(con_q).values('id', 'status')
            response.data = {'data_list': list(obj_list)}

        return JsonResponse(response.__dict__)


