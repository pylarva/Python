#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import time
import paramiko
import threading
from multiprocessing import Process
from repository import models
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse


from web.service import asset

data_dict = {'status': False, 'message': ""}


class VirtualListView(View):
    def get(self, request, *args, **kwargs):
        data = models.VirtualMachines.objects.all()
        host = models.HostMachines.objects.all()
        machine_type = models.MachineType.objects.all()
        return render(request, 'virtual_list.html', {'data': data, 'host_list': host, 'machine_type': machine_type})

    def post(self, request, *args, **kwargs):
        v = request.POST.get('host_machine')
        new_name = request.POST.get('new_host_name')
        new_ip = request.POST.get('new_host_ip')
        machine_type = request.POST.get('machine_type')
        print(v, new_ip, new_name, machine_type)

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.162.2', port=22, username='root', key_filename='/Users/pylarva/.ssh/id_rsa', timeout=3)
            stdin, stdout, stderr = ssh.exec_command('df')
            result = stdout.read()
            print(result)
            ssh.close()

            # 创建进程去执行任务
            ip = '192.168.162.2'
            p = Process(target=self.foo, args=(ip, ))
            p.start()

        except Exception:

            data_dict['status'] = False
            data_dict['message'] = "宿主机连接失败 请检查网络 ssh_key 公钥验证是否正常..."

            return HttpResponse(json.dumps(data_dict))

        models.VirtualMachines.objects.create(mudroom_host=v, host_name=new_name, host_ip=new_ip, machine_type_id=machine_type)

        data_dict['status'] = True
        data_dict['message'] = "ok"

        ret = HttpResponse(json.dumps(data_dict))
        ret.set_cookie('mess', '200', max_age=5)
        return ret

    def foo(self, ip):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=22, username='root', key_filename='/Users/pylarva/.ssh/id_rsa', timeout=3)
        stdin, stdout, stderr = ssh.exec_command('ls')
        result = stdout.read()
        print(result)

        virsh_cmd = 'virt-clone --connect=qemu:///system -o a0-kvm-vhost-38-115.yh -n a0-kvm-vhost-38-119.yh -f /opt/mv/a0-kvm-vhost-38-119.yh.qcow2'
        stdin, stdout, stderr = ssh.exec_command(virsh_cmd)
        result = stdout.read()
        print('拷贝文件...', result)
        time.sleep(5)

        virsh_cmd = 'virsh start a0-kvm-vhost-38-119.yh'
        stdin, stdout, stderr = ssh.exec_command(virsh_cmd)
        result = stdout.read()
        print('启动虚拟机...', result)
        time.sleep(30)

        data = os.system("ping -c 1 192.168.31.115 > /dev/null 2>&1")
        if data == 0:
            self.chang_ip()
            print('启动成功...')
        else:
            print('lost...')

        ssh.close()


    def exec_task(self, ssh):
        virsh_cmd = 'virt-clone --connect=qemu:///system -o a0-kvm-vhost-38-115.yh -n a0-kvm-vhost-38-119.yh -f /opt/mv/a0-kvm-vhost-38-119.yh.qcow2'
        stdin, stdout, stderr = ssh.exec_command(virsh_cmd)
        result = stdout.read()
        print('拷贝文件...', result)
        time.sleep(5)

        virsh_cmd = 'virsh start a0-kvm-vhost-38-119.yh'
        stdin, stdout, stderr = ssh.exec_command(virsh_cmd)
        result = stdout.read()
        print('启动虚拟机...', result)
        time.sleep(30)

        data = os.system("ping -c 1 192.168.31.115 > /dev/null 2>&1")
        if data == 0:
            self.chang_ip()
            print('启动成功...')
        else:
            print('lost...')

    def chang_ip(self):

        transport = paramiko.Transport(('192.168.31.115', 22))
        transport.connect(username='root', password='123456')
        ssh = paramiko.SSHClient()
        ssh._transport = transport

        print('更改ip...')
        stdin, stdout, stderr = ssh.exec_command(
            "sed -i 's#192.168.31.115#192.168.31.119#g' /etc/sysconfig/network-scripts/ifcfg-eth0")
        result = stdout.read()
        print('IP完成...', result)
        stdin, stdout, stderr = ssh.exec_command("ifdown eth0 && ifup eth0", timeout=1)
        result = stdout.read()
        print('虚机部署完成...', result)
        transport.close()


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
    def get(self, request, device_type_id, asset_nid):
        response = asset.Asset.assets_detail(device_type_id, asset_nid)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class AddAssetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_asset.html')