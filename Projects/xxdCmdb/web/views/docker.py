#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import json
import docker
import subprocess
from django.views import View
from netaddr import IPNetwork
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
from conf import kvm_config
from conf import jenkins_config



# @method_decorator(auth_admin, name='dispatch')
class DockerView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(DockerView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        data = models.DockerNode.objects.all()
        business_2 = models.BusinessTwo.objects.all()
        return render(request, 'docker_index.html', {'data': data, 'business_2': business_2})

    def post(self, request):
        response = BaseResponse()
        response.data = []

        is_create = request.POST.get('is_create')
        if is_create:
            self.container_create(request)

        # 检查容器名称是否重复 && 分配IP地址 && 确认容器挂载路径
        check_container_name = request.POST.get('check_container_name')
        if check_container_name:
            print(check_container_name)
            ip = request.POST.get('ip')
            c = docker.Client(base_url='tcp://%s:2375' % ip, version='auto', timeout=5)
            container_list = c.containers(quiet=False, all=True, trunc=True, latest=False, since=None,
                                          before=None, limit=-1)
            response.status = True
            # 检测到相同容器名就退出
            check_container_name = '/%s' % check_container_name
            for item in container_list:
                if check_container_name == item['Names'][0]:
                    response.status = False
                    response.error = '容器名已存在!'
                    return JsonResponse(response.__dict__)

            # 分配IP地址
            container_ip = request.POST.get('container_ip')
            if container_ip == 'auto':
                try:
                    container_new_ip = self.get_ip(ip)
                except Exception as e:
                    print(e)
                    response.status = False
                    response.error = '自动获取IP地址失败...'
                    return JsonResponse(response.__dict__)
                response.data.append(str(container_new_ip))

            # 设置挂载路径
            container_business = request.POST.get('container_business')
            if container_business:
                container_app_name = request.POST.get('container_app_name')
                if container_business == 'no' and container_app_name == 'no':
                    response.data.append('no')
                    response.data.append('no')
                    return JsonResponse(response.__dict__)
                else:
                    print(container_business, container_app_name)
                    mount_inside = jenkins_config.container_mount_inside.replace('AAA', container_app_name)
                    mount_outside = jenkins_config.container_mount_outside.replace('AAA', container_business).replace('BBB', container_app_name)
                    response.data.append(mount_inside)
                    response.data.append(mount_outside)
                    print(response.data)

            return JsonResponse(response.__dict__)

        # 前端请求主机容器上面的镜像
        host_ip = request.POST.get('ip')
        if host_ip:
            try:
                c = docker.Client(base_url='tcp://%s:2375' % host_ip, version='auto', timeout=5)
            except Exception as e:
                response.error = '连接%s超时...' % host_ip
                print(e)
                response.status = False
                return JsonResponse(response.__dict__)
            response.data = c.images()
            response.status = True
        return JsonResponse(response.__dict__)

    def container_create(self, request):
        """
        创建容器
        :param request:
        :return:
        """
        response = BaseResponse()
        response.status = True
        create_node = request.POST.get('create_node')
        create_image = request.POST.get('create_image')
        create_name = request.POST.get('create_name')
        create_ip = request.POST.get('create_ip')
        create_cpu = request.POST.get('create_cpu')
        create_memory = request.POST.get('create_memory')
        create_mount_in = request.POST.get('create_mount_in')
        create_mount_out = request.POST.get('create_mount_out')
        docker_info = request.POST.get('docker_info')

        host_name = jenkins_config.container_host_name.replace('A', create_ip.split('.')[-2]).replace('B', create_ip.split('.')[-1])
        new_gateway = '%s.%s' % ('.'.join(create_ip.split('.')[0:3]), jenkins_config.container_gateway_ip)

        # 创建容器
        try:
            c = docker.Client(base_url='tcp://%s:2375' % create_node, version='auto', timeout=10)

            # 需要挂载
            if create_mount_in and create_mount_out:

                host_config = c.create_host_config(binds={create_mount_out: {'bind': create_mount_in, 'ro': False}},
                                                   mem_limit='%sg' % create_memory, cpu_period=int('%s00000' % create_cpu),
                                                   cpu_quota=int('%s00000' % create_cpu * 2))
                c_ret = c.create_container(create_image, hostname=host_name, user=None,
                                           detach=True, stdin_open=True, tty=True,
                                           ports=None, environment=None, dns=None,
                                           volumes=[create_mount_out],
                                           host_config=host_config,
                                           volumes_from=None, network_disabled=False, name=create_name,
                                           entrypoint=None, cpu_shares=None, working_dir=None)
                c.start(c_ret['Id'])

            # 不需要挂载
            else:
                c_ret = c.create_container(create_image, hostname=host_name, user=None,
                                           detach=True, stdin_open=True, tty=True,
                                           ports=None, environment=None, dns=None,
                                           volumes_from=None, network_disabled=False, name=create_name,
                                           entrypoint=None, cpu_shares=None, working_dir=None)
                c.start(c_ret['Id'])

            # 分配IP
            cmd_shell = 'ssh root@%s pipework br0 %s %s/24@%s' % (create_node, create_name, create_ip, new_gateway)
            self.set_ip(cmd_shell)

            # 资产入库
            models.Asset.objects.create(host_ip=create_ip, host_name=host_name, host_type=5, host_machine=create_node,
                                        host_cpu=create_cpu, host_memory=create_memory)
            # 容器信息记录表
            models.DockerInfo.objects.create(name=create_name, ip=create_ip, create_user=request.session['username'],
                                             docker_info=docker_info)
        except Exception as e:
            response.status = False
            print(e)
            response.error = str(e)

        time.sleep(5)
        return JsonResponse(response.__dict__)

    def get_ip(self, host_machine):
        """
        自动获取IP地址
        :param host_machine:
        :return:
        """
        ipaddr = IPNetwork('%s/24' % host_machine)[kvm_config.kvm_range_ip[0]:kvm_config.kvm_range_ip[1]]
        for ip in ipaddr:
            s = subprocess.call("ssh root@%s 'ping -c1 -W 1 %s > /dev/null'" % (host_machine, ip), shell=True)
            if s != 0:
                num = models.Asset.objects.filter(host_ip=ip).count()
                if num == 0:
                    return ip
        return False

    def set_ip(self, cmd_shell):
        """
        远程设置容器IP地址
        :param cmd_shell:
        :return:
        """
        print(cmd_shell)
        try:
            subprocess.Popen(cmd_shell, stdin=subprocess.PIPE, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            time.sleep(2)
        except Exception as e:
            print(e)
        return True


class DockersView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(DockersView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        data = models.DockerNode.objects.all()
        return render(request, 'dockers.html', {'data': data})

    def post(self, request):
        # 操作容器
        is_handle = request.POST.get('is_handle')
        if is_handle:
            response = self.container_handle(request)
            return JsonResponse(response.__dict__)

        # 页面返回容器详细信息
        host_ip = request.POST.get('ip')
        if host_ip:
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

            cmd = "ssh root@%s docker exec %s ifconfig | awk 'NR==10 {print $2}'" % (host_ip, i['Names'])
            try:
                ret = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                i['NewIp'] = ret.stdout.read().strip()
            except Exception as e:
                i['NewIp'] = ''

        response.status = True
        return response

    def container_handle(self, request):
        """
        操作容器
        :param request:
        :return:
        """
        response = BaseResponse()
        response.status = True
        ip = request.POST.get('ip')
        name = request.POST.get('name')
        cmd = request.POST.get('cmd')
        nip = request.POST.get('nip')

        c = docker.Client(base_url='tcp://%s:2375' % ip, version='auto', timeout=10)

        # 开启或者重启容器
        if cmd == 'power':
            current_status = c.inspect_container(name).get('State').get('Status')
            print(c.inspect_container(name))
            if current_status == 'running':
                c.stop(name)
            else:
                c.start(name)
                # 根据容器名重新设置容器的IP地址
                try:
                    old_ip = c.inspect_container(name).get('Config').get('Hostname').split('-')[-1].split('.')[0]
                except Exception as e:
                    response.status = False
                    response.error = '容器主机名中未检测到末尾的IP的地址信息...'
                    return response
                new_ip = '%s.%s' % ('.'.join(ip.split('.')[0:3]), old_ip)
                new_gateway = '%s.%s' % ('.'.join(ip.split('.')[0:3]), '253')
                cmd_shell = 'ssh root@%s pipework br0 %s %s/24@%s' % (ip, name, new_ip, new_gateway)
                self.set_ip(cmd_shell)

        # 给容器设置新的IP地址
        if cmd == 'set_ip':
            ip_type = request.POST.get('ip_type')
            # 自动设置Ip地址
            if ip_type == 'auto':
                new_ip = self.get_ip(ip)
                print(new_ip)
                new_gateway = '%s.%s' % ('.'.join(ip.split('.')[0:3]), '253')
                c.restart(name)
                cmd_shell = 'ssh root@%s pipework br0 %s %s/24@%s' % (ip, name, new_ip, new_gateway)
                self.set_ip(cmd_shell)

                # 自动设置完IP后需要修改主机名
                get_old_ip = c.inspect_container(name).get('Config').get('Hostname').split('-')[-1]
                a = c.inspect_container(name).get('Config').get('Hostname')
                new_hostname = a.replace(get_old_ip, str(new_ip).split('.')[-1])
                cmd_shell = 'ssh root@%s docker exec %s hostname %s' % (ip, name, new_hostname)
                self.set_ip(cmd_shell)

        # 重启容器
        if cmd == 'restart':
            c.restart(name)
            # 根据容器名重新设置容器的IP地址
            try:
                old_ip = c.inspect_container(name).get('Config').get('Hostname').split('-')[-1].split('.')[0]
            except Exception as e:
                response.status = False
                response.error = '容器主机名中未检测到末尾的IP的地址信息...'
                return response
            new_ip = '%s.%s' % ('.'.join(ip.split('.')[0:3]), old_ip)
            new_gateway = '%s.%s' % ('.'.join(ip.split('.')[0:3]), '253')
            cmd_shell = 'ssh root@%s pipework br0 %s %s/24@%s' % (ip, name, new_ip, new_gateway)
            self.set_ip(cmd_shell)

        # 删除容器
        if cmd == 'delete':
            try:
                c.remove_container(name)
                # 删除资产 (从容器信息查询表获取容器IP)
                obj = models.DockerInfo.objects.filter(name=name).count()
                if obj:
                    nip = models.DockerInfo.objects.filter(name=name).first().ip
                    models.Asset.objects.filter(host_ip=nip).delete()
                    models.DockerInfo.objects.filter(name=name).delete()
                    print('delete docker...%s' % nip)
            except Exception as e:
                response.status = False
                response.error = str(e)
                return response

        response = self.container_inspect(ip)
        return response

    def get_ip(self, host_machine):
        """
        自动获取IP地址
        :param host_machine:
        :return:
        """
        ipaddr = IPNetwork('%s/24' % host_machine)[kvm_config.kvm_range_ip[0]:kvm_config.kvm_range_ip[1]]
        for ip in ipaddr:
            s = subprocess.call("ssh root@%s 'ping -c1 -W 1 %s > /dev/null'" % (host_machine, ip), shell=True)
            if s != 0:
                num = models.Asset.objects.filter(host_ip=ip).count()
                if num == 0:
                    return ip
        return False

    def set_ip(self, cmd_shell):
        """
        远程设置容器IP地址
        :param cmd_shell:
        :return:
        """
        print(cmd_shell)
        try:
            subprocess.Popen(cmd_shell, stdin=subprocess.PIPE, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            time.sleep(2)
        except Exception as e:
            print(e)
        return True


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
