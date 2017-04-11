#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import time
import paramiko
import queue
from multiprocessing import Pool
from multiprocessing import Process
from multiprocessing import queues
import multiprocessing
from repository import models
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from xml.etree import ElementTree as ET

from conf import kvm_config
from web.service import asset

data_dict = {'status': False, 'message': ""}


class VirtualListView(View):
    def get(self, request, *args, **kwargs):
        data = models.VirtualMachines.objects.all()
        host = models.HostMachines.objects.all()
        machine_type = models.MachineType.objects.all()
        return render(request, 'virtual_list.html', {'data': data, 'host_list': host, 'machine_type': machine_type})

    def post(self, request, *args, **kwargs):
        host_machine = request.POST.get('host_machine')
        new_ip = request.POST.get('new_host_ip')
        machine_type = request.POST.get('machine_type')
        memory_num = request.POST.get('memory_num')
        cpu_num = request.POST.get('cpu_num')
        new_name = 'a0-kvm-vhost-%s-%s' % (new_ip.split('.')[-2], new_ip.split('.')[-1])
        print(host_machine, new_ip, new_name, machine_type, memory_num, cpu_num)

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host_machine, port=22, username='root', key_filename=kvm_config.ssh_key_file, timeout=kvm_config.ssh_timeout)
            stdin, stdout, stderr = ssh.exec_command('df')
            result = stdout.read()
            print(result)
            ssh.close()

            # 创建进程去执行任务
            p = Process(target=self.exec_task, args=(host_machine, new_name, new_ip, machine_type, cpu_num, memory_num))
            p.start()
            # pool.apply(func=self.exec_task, args=(host_machine, new_name, new_ip, machine_type, cpu_num, memory_num))
            # pool.close()
            # pool.join()

        except Exception:

            data_dict['status'] = False
            data_dict['message'] = "Host machine connect failed..."

            return HttpResponse(json.dumps(data_dict))

        models.VirtualMachines.objects.create(mudroom_host=host_machine, host_name=new_name, host_ip=new_ip,
                                              machine_type_id=machine_type, cpu_num=cpu_num, memory_num=memory_num)

        data_dict['status'] = True
        data_dict['message'] = "ok"

        ret = HttpResponse(json.dumps(data_dict))
        # 设置一个cookie值 引导前端进度条执行
        ret.set_cookie('mess', '200', max_age=5)
        return ret

    def exec_task(self, host_machine, host_name, new_ip, machine_type, cpu_num, memory_num):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_machine, port=22, username='root', key_filename=kvm_config.ssh_key_file, timeout=kvm_config.ssh_timeout)
        stdin, stdout, stderr = ssh.exec_command('ls')
        result = stdout.read()
        print(result)

        template_mirror = kvm_config.CentOS_6[machine_type]
        new_mirror = kvm_config.kvm_qcow_dir + host_name + '.qcow2'

        # 1、拷贝镜像文件
        cmd = 'cp %s %s' % (template_mirror, new_mirror)
        ssh.exec_command(cmd)
        time.sleep(10)
        print(cmd)

        # 2、新建并修改xml文件
        new_xml_path = self.change_cpu_memory(host_name, cpu_num, memory_num, new_mirror)
        cmd = 'scp %s root@%s:%s' % (new_xml_path, host_machine, kvm_config.host_xml_path)
        os.system(cmd)
        print(cmd)

        # 3、define虚拟机
        xml_file = '/opt/xml/' + host_name + '.xml'
        cmd = 'virsh define %s' % xml_file
        ssh.exec_command(cmd)
        print(cmd)

        # 4、修改网卡配置文件
        cmd = 'mkdir /opt/data/%s' % host_name
        ssh.exec_command(cmd)
        print(cmd)
        cmd = 'cp /opt/data/ifcfg-eth0 /opt/data/%s/' % host_name
        ssh.exec_command(cmd)
        print(cmd)
        cmd = 'cp /opt/data/70-persistent-net.rules /opt/data/%s/' % host_name
        ssh.exec_command(cmd)
        print(cmd)
        cmd = "sed -i 's#%s#%s#g' /opt/data/%s/ifcfg-eth0" % (kvm_config.kvm_template_ip, new_ip, host_name)
        ssh.exec_command(cmd)
        print(cmd)
        cmd = "virt-copy-in -d %s /opt/data/%s/ifcfg-eth0 /etc/sysconfig/network-scripts/" % (host_name, host_name)
        ssh.exec_command(cmd)
        time.sleep(10)
        print(cmd)
        cmd = 'virt-copy-in -d %s /opt/data/%s/70-persistent-net.rules /etc/udev/rules.d/' % (host_name, host_name)
        ssh.exec_command(cmd)
        time.sleep(10)
        print(cmd)

        # 5、启动虚拟机
        cmd = 'virsh start %s' % host_name
        ssh.exec_command(cmd)
        print(cmd)

        # virsh_cmd = 'virt-clone --connect=qemu:///system -o %s -n %s -f %s.qcow2' % (template_mirror, host_name,
        #                                                                              new_mirror)

        # print(virsh_cmd)
        # stdin, stdout, stderr = ssh.exec_command(virsh_cmd)
        # result = stdout.read()
        # print('拷贝文件...', result)
        # time.sleep(5)

        # virsh_cmd = 'virsh start %s' % host_name
        # print(virsh_cmd)
        # stdin, stdout, stderr = ssh.exec_command(virsh_cmd)
        # result = stdout.read()
        # print('启动虚拟机...', result)
        # time.sleep(30)

        # data = os.system("ping -c 1 192.168.31.115 > /dev/null 2>&1")
        # if data == 0:
        #     self.chang_ip(new_ip)
        #     print('启动成功...')
        # else:
        #     print('lost...')

        ssh.close()

    def chang_ip(self, new_ip):

        transport = paramiko.Transport(('192.168.31.115', 22))
        transport.connect(username='root', password='123456')
        ssh = paramiko.SSHClient()
        ssh._transport = transport

        print('更改ip...')
        stdin, stdout, stderr = ssh.exec_command(
            "sed -i 's#192.168.31.115#%s#g' /etc/sysconfig/network-scripts/ifcfg-eth0" % new_ip)
        result = stdout.read()
        print('IP完成...', result)
        stdin, stdout, stderr = ssh.exec_command("ifdown eth0 && ifup eth0", timeout=1)
        # result = stdout.read()
        print('虚机部署完成...', result)
        transport.close()

    def change_cpu_memory(self, host_name, new_cpu, new_memory,  new_mirror):
        template_xml_file = kvm_config.kvm_template_xml

        tree = ET.parse(template_xml_file)
        root = tree.getroot()

        new_memory = str(new_memory) + '388608'

        for node in root.iter('name'):
            # new_name = int(host_name)
            node.text = str(host_name)

        for node in root.iter('vcpu'):
            new_cpu = int(new_cpu)
            node.text = str(new_cpu)

        for node in root.iter('memory'):
            new_memory = int(new_memory)
            node.text = str(new_memory)

        for node in root.iter('currentMemory'):
            new_memory = int(new_memory)
            node.text = str(new_memory)

        root[10][1][1].attrib['file'] = new_mirror

        tree = ET.ElementTree(root)
        xml_path = kvm_config.kvm_template_xml_dir + host_name + '.xml'
        tree.write(xml_path, encoding='utf-8')

        return xml_path


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