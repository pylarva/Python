#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import time
import paramiko
from repository import models
from django.views import View
from multiprocessing import Process
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from xml.etree import ElementTree as ET
from utils import pagination

from conf import kvm_config
from web.service import asset

data_dict = {'status': False, 'message': ""}


class VirtualListView(View):
    def get(self, request, *args, **kwargs):
        data = models.VirtualMachines.objects.all()
        host = models.HostMachines.objects.all()
        machine_type = models.MachineType.objects.all()

        data_total = models.VirtualMachines.objects.all().count()
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)
        print(current_page)

        val = request.COOKIES.get('per_page_count', 10)
        page_init = {}
        page_init['per_page_count'] = val
        print(val)
        val = int(val)

        page_obj = pagination.Page(current_page, data_total, val)
        data = data[page_obj.start:page_obj.end]
        page_str = page_obj.page_str('virtual_list.html')

        return render(request, 'virtual_list.html', {'data': data, 'host_list': host, 'machine_type': machine_type,
                                                     'page_str': page_str, 'page_init': page_init})

    def post(self, request, *args, **kwargs):

        change_id = request.POST.get('change_id', None)

        # ajax请求对应主机名
        if change_id:
            print(change_id)
            change_data = models.VirtualMachines.objects.filter(id=change_id).first()
            data_dict['id'] = change_id
            data_dict['hostname'] = change_data.host_name
            data_dict['status'] = True

            return HttpResponse(json.dumps(data_dict))

        change_hostname = request.POST.get('change_hostname', None)

        if change_hostname:
            change_id = request.POST.get('change_iid', None)
            self.change_host_name(change_id, change_hostname)
            data_dict['status'] = True
            return HttpResponse(json.dumps(data_dict))

        host_del_id = request.POST.get('host_del_id', None)
        if host_del_id:
            try:
                # 删除目标虚拟机
                print('del_id', host_del_id)
                self.host_del(host_del_id)

            except Exception as e:
                data_dict['status'] = False
                data_dict['message'] = "虚拟机删除失败！"
                return HttpResponse(json.dumps(data_dict))

            data_dict['status'] = True
            data_dict['message'] = "虚拟机删除成功！"
            return HttpResponse(json.dumps(data_dict))

        host_machine = request.POST.get('host_machine')
        new_ip = request.POST.get('new_host_ip')
        machine_type = request.POST.get('machine_type')
        memory_num = request.POST.get('memory_num')
        cpu_num = request.POST.get('cpu_num')
        new_name = 'a0-kvm-vhost-%s-%s.yh' % (new_ip.split('.')[-2], new_ip.split('.')[-1])
        new_gateway = new_ip.split('.')
        new_gateway = new_gateway[0] + '.' + new_gateway[1] + '.' + new_gateway[2] + '.' + '253'
        print(host_machine, new_ip, new_name, machine_type, memory_num, cpu_num, new_gateway)

        ip_num = models.VirtualMachines.objects.filter(host_ip=new_ip).count()

        if ip_num:
            data_dict['status'] = False
            data_dict['message'] = "IP地址已经存在 不允许重复装机！"
            return HttpResponse(json.dumps(data_dict))

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host_machine, port=22, username='root', key_filename=kvm_config.ssh_key_file, timeout=kvm_config.ssh_timeout)
            stdin, stdout, stderr = ssh.exec_command('ip addr | grep %s' % host_machine)
            br_name = stdout.read()
            br_name = str(br_name, encoding='utf-8').split(' ')[-1].split('\n')[0]
            ssh.close()

            # 创建进程去执行任务
            # p = Process(target=self.exec_task, args=(host_machine, new_name, new_ip, machine_type, cpu_num, memory_num, br_name, new_gateway))
            # p.start()

        except Exception:

            data_dict['status'] = False
            data_dict['message'] = "宿主机连接失败！请确认已在目标宿主机增加SSH_key公钥验证！"

            return HttpResponse(json.dumps(data_dict))

        models.VirtualMachines.objects.create(mudroom_host=host_machine, host_name=new_name, host_ip=new_ip,
                                              machine_type_id=machine_type, cpu_num=cpu_num, memory_num=memory_num)

        data_dict['status'] = True
        data_dict['message'] = "ok"

        ret = HttpResponse(json.dumps(data_dict))
        # 设置一个cookie值 引导前端进度条执行
        ret.set_cookie('mess', '200', max_age=5)
        return ret

    def exec_task(self, host_machine, host_name, new_ip, machine_type, cpu_num, memory_num, br_name, new_gateway):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_machine, port=22, username='root', key_filename=kvm_config.ssh_key_file, timeout=kvm_config.ssh_timeout)
        stdin, stdout, stderr = ssh.exec_command('ls')
        result = stdout.read()
        print(result)

        template_mirror = kvm_config.CentOS_6[machine_type]
        system_version = template_mirror[20]
        print(system_version)
        new_mirror = kvm_config.kvm_qcow_dir + host_name + '.qcow2'

        # 1、拷贝镜像文件
        cmd = 'cp %s %s' % (template_mirror, new_mirror)
        ssh.exec_command(cmd)
        time.sleep(10)
        print(cmd)

        # 2、新建并修改xml文件
        new_xml_path = self.change_cpu_memory(host_name, cpu_num, memory_num, new_mirror, br_name)
        cmd = 'scp %s root@%s:%s' % (new_xml_path, host_machine, kvm_config.kvm_xml_dir)
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
        cmd = 'cp /opt/data/network /opt/data/%s/' % host_name
        ssh.exec_command(cmd)
        print(cmd)
        cmd = "sed -i 's#%s#%s#g' /opt/data/%s/ifcfg-eth0" % (kvm_config.kvm_template_ip, new_ip, host_name)
        ssh.exec_command(cmd)
        print(cmd)
        cmd = "sed -i 's#%s#%s#g' /opt/data/%s/ifcfg-eth0" % ('192.168.31.253', new_gateway, host_name)
        ssh.exec_command(cmd)
        print(cmd)
        cmd = "sed -i 's#%s#%s#g' /opt/data/%s/network" % (kvm_config.kvm_template_hostname, host_name, host_name)
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
        cmd = 'virt-copy-in -d %s /opt/data/%s/network /etc/sysconfig/' % (host_name, host_name)
        ssh.exec_command(cmd)
        time.sleep(10)
        print(cmd)

        # 5、启动虚拟机
        cmd = 'virsh start %s' % host_name
        ssh.exec_command(cmd)
        print(cmd)

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

    def change_cpu_memory(self, host_name, new_cpu, new_memory,  new_mirror, br_name):
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
        root[10][8][0].attrib['bridge'] = br_name

        tree = ET.ElementTree(root)
        xml_path = kvm_config.kvm_template_xml_dir + host_name + '.xml'
        tree.write(xml_path, encoding='utf-8')

        return xml_path

    def host_del(self, host_del_id):

        obj = models.VirtualMachines.objects.filter(id=host_del_id)
        print(obj[0].host_name, obj[0].mudroom_host)
        host_name = obj[0].host_name
        host_machine = obj[0].mudroom_host

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_machine, port=22, username='root', key_filename=kvm_config.ssh_key_file,
                    timeout=kvm_config.ssh_timeout)
        stdin, stdout, stderr = ssh.exec_command('ls')
        result = stdout.read()
        print(result)

        mirror_file = kvm_config.kvm_qcow_dir + host_name + '.qcow2'
        print(mirror_file)

        cmd = 'virsh destroy %s' % host_name
        ssh.exec_command(cmd)
        print(cmd)
        cmd = 'virsh undefine %s' % host_name
        ssh.exec_command(cmd)
        print(cmd)

        # 是否删除镜像
        # cmd = 'rm -f %s' % mirror_file
        # ssh.exec_command(cmd)
        # print(cmd)

        models.VirtualMachines.objects.filter(id=host_del_id).delete()

    def change_host_name(self, host_id, host_name):
        models.VirtualMachines.objects.filter(id=host_id).update(host_name=host_name)
        obj = models.VirtualMachines.objects.filter(id=host_id)
        host_ip = obj[0].host_ip

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_ip, port=22, username='root', password='xinxindai318', timeout=kvm_config.ssh_timeout)

        # 开始更新主机名
        str_host = host_ip + '    ' + host_name
        cmd = "hostname %s && echo %s > /etc/hostname && \
                    echo %s >> /etc/hosts && \
                    sed -i s/HOSTNAME=.*/HOSTNAME=%s/g /etc/sysconfig/network && \
                    service zabbix_agentd restart && \
                    service rsyslog restart &" % (host_name, host_name, str_host, host_name)
        ssh.exec_command(cmd)


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