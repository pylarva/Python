#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import time
import paramiko
import subprocess
from netaddr import IPNetwork
from repository import models
from django.views import View
from multiprocessing import Process
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.utils.decorators import method_decorator
from xml.etree import ElementTree as ET
from utils import pagination

from conf import kvm_config
from web.service import asset

data_dict = {'status': False, 'message': ""}

USER_NAME = {}


def auth(func):
    def inner(request, *args, **kwargs):
        # v = request.COOKIES.get('user_cookie')
        v = request.session.get('is_login', None)
        # print(v)
        if not v:
            return redirect('login.html')
        global USER_NAME
        USER_NAME['name'] = v
        return func(request, *args, **kwargs)
    return inner


@method_decorator(auth, name='dispatch')
class VirtualListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(VirtualListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # data = models.Asset.objects.all()
        # data_status = models.Asset.device_status_choices
        # print(data_status)
        data = models.VirtualMachines.objects.all().order_by('-id')
        host = models.HostMachines.objects.all()
        machine_type = models.MachineType.objects.all()

        # data_total = models.Asset.objects.all().count()
        data_total = models.VirtualMachines.objects.all().count()
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)
        # print(current_page)

        val = request.COOKIES.get('per_page_count', 1000)
        page_init = {}
        page_init['per_page_count'] = val
        # print(val)
        val = int(val)

        page_obj = pagination.Page(current_page, data_total, val)
        data = data[page_obj.start:page_obj.end]
        page_str = page_obj.page_str('virtual_list.html')

        return render(request, 'virtual_list.html', {'data': data, 'host_list': host, 'machine_type': machine_type,
                                                     'page_str': page_str, 'page_init': page_init})

    def post(self, request, *args, **kwargs):
        host_machine = request.POST.get('host_machine')

        # 自动获取IP地址
        get_new_ip = request.POST.get('get_new_ip', None)
        if get_new_ip:
            new_ip = self.get_ip(host_machine)
            new_ip = str(new_ip)
            if not new_ip:
                data_dict['status'] = False
                data_dict['message'] = "未分配到可用IP地址..."
                return HttpResponse(json.dumps(data_dict))
            else:
                data_dict['status'] = True
                data_dict['message'] = new_ip
                return HttpResponse(json.dumps(data_dict))

        # 前端来获取宿主机信息
        host = request.POST.get('host', None)
        if host:
            cmd = "ssh root@%s 'virsh list --all'" % host
            result = os.popen(cmd).readlines()
            cmd_all_memory = "free -m | awk 'NR==2{print $2}'"
            cmd_1 = "ps -ef |grep kvm | awk '{print $1,$16}'|awk '{print $2}'|awk '{sum += $1} END {print sum}'"
            cmd_2 = "ps -ef |grep kvm | awk '{print $1,$20}'|awk '{print $2}'|awk -F ',' '{print $1}'|awk '{sum += $1} END {print sum}'"
            if host == '192.168.38.190':
                cmd_1 = "ps -ef |grep kvm | awk '{print $1,$15}'|awk '{print $2}'|awk '{sum += $1} END {print sum}'"
                cmd_2 = "ps -ef |grep kvm | awk '{print $1,$19}'|awk '{print $2}'|awk -F ',' '{print $1}'|awk '{sum += $1} END {print sum}'"
            if host == '192.168.38.200' or host == '192.168.38.250' or host == '192.168.50.51':
                cmd_2 = "ps -ef |grep kvm | awk '{print $1,$18}'|awk '{print $2}'|awk -F ',' '{print $1}'|awk '{sum += $1} END {print sum}'"
            if result:
                cmd_memory = "ssh root@%s %s" % (host, cmd_1)
                memory_sum = os.popen(cmd_memory).readlines()
                cmd_cpu = "ssh root@%s %s" % (host, cmd_2)
                cpu_sum = os.popen(cmd_cpu).readlines()
                cmd_total_memory = "ssh root@%s %s" % (host, cmd_all_memory)
                total_memory = os.popen(cmd_total_memory).readlines()
                data_dict['status'] = True
                data_dict['data'] = result
                data_dict['memory'] = memory_sum
                data_dict['cpu'] = cpu_sum
                data_dict['total_memory'] = total_memory
                return HttpResponse(json.dumps(data_dict))
            else:
                data_dict['status'] = False
                return HttpResponse(json.dumps(data_dict))

        # 前端switch开关请求模版主机IP
        template_id = request.POST.get('template_id', None)
        if template_id:
            template_obj = models.MachineType.objects.filter(id=template_id).first()

            template_status = request.POST.get('template_status', None)
            # 开启关闭模版机
            self.turn_on_off_template(template_id, template_status)

            data_dict['template_ip'] = template_obj.machine_ip
            data_dict['status'] = True
            return HttpResponse(json.dumps(data_dict))

        # ajax请求对应主机名
        change_id = request.POST.get('change_id', None)
        if change_id:
            # print(change_id)
            # change_data = models.Asset.objects.filter(id=change_id).first()
            change_data = models.VirtualMachines.objects.filter(id=change_id).first()
            data_dict['id'] = change_id
            data_dict['hostname'] = change_data.host_name
            data_dict['status'] = True
            return HttpResponse(json.dumps(data_dict))

        # 新增镜像
        new_mirror_id = request.POST.get('new_id', None)
        if new_mirror_id:
            mirror_name = request.POST.get('mirror_name', None)
            mirror_ip = request.POST.get('mirror_ip', None)
            self.add_new_mirror(new_mirror_id, mirror_name, mirror_ip)
            data_dict['status'] = True
            return HttpResponse(json.dumps(data_dict))

        # 修改主机名
        change_hostname = request.POST.get('change_hostname', None)
        if change_hostname:
            change_id = request.POST.get('change_iid', None)
            self.change_host_name(change_id, change_hostname)
            data_dict['status'] = True
            return HttpResponse(json.dumps(data_dict))

        # 删除主机
        host_del_id = request.POST.get('host_del_id', None)
        if host_del_id:
            try:
                # 删除目标虚拟机
                self.host_del(host_del_id)

            except Exception as e:
                data_dict['status'] = False
                data_dict['message'] = "虚拟机删除失败！"
                return HttpResponse(json.dumps(data_dict))

            data_dict['status'] = True
            data_dict['message'] = "虚拟机删除成功！"
            return HttpResponse(json.dumps(data_dict))

        machine_type = request.POST.get('machine_type')
        memory_num = request.POST.get('memory_num')
        cpu_num = request.POST.get('cpu_num')
        new_gateway_list = host_machine.split('.')
        new_gateway = new_gateway_list[0] + '.' + new_gateway_list[1] + '.' + new_gateway_list[2] + '.' + kvm_config.kvm_last_gateway

        new_ip = request.POST.get('new_host_ip', None)

        # 如果前端没有传来新IP地址 先对IP地址作标记 然后在进程里面再自动或去IP地址
        # if not new_ip:
        #     new_ip = self.get_ip(host_machine)
        #     new_ip = str(new_ip)
        #     if not new_ip:
        #         data_dict['status'] = False
        #         data_dict['message'] = "未分配到可用IP地址..."
        #         return HttpResponse(json.dumps(data_dict))

        new_name = '%s-kvm-vhost-%s-%s.%s' % (kvm_config.kvm_addr, new_ip.split('.')[-2], new_ip.split('.')[-1], kvm_config.kvm_str)
        template_mirror_obj = models.MachineType.objects.filter(id=machine_type).first()
        template_mirror = template_mirror_obj.machine_type

        print(host_machine, new_ip, new_name, machine_type, memory_num, cpu_num, new_gateway)

        # ip_num = models.Asset.objects.filter(host_ip=new_ip).count()
        ip_num_a = models.VirtualMachines.objects.filter(host_ip=new_ip).count()
        ip_num_b = models.Asset.objects.filter(host_ip=new_ip).count()

        if ip_num_a or ip_num_b:
            data_dict['status'] = False
            data_dict['message'] = "IP地址在总资产表中已经存在 不允许重复装机！"
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
            p = Process(target=self.exec_task, args=(host_machine, new_name, new_ip, cpu_num, memory_num, br_name, new_gateway, template_mirror))
            p.start()

        except Exception:

            data_dict['status'] = False
            data_dict['message'] = "宿主机连接失败！请确认已在目标宿主机增加SSH_key公钥验证！"

            return HttpResponse(json.dumps(data_dict))

        models.VirtualMachines.objects.create(mudroom_host=host_machine, host_name=new_name, host_ip=new_ip,
                                              machine_type_id=machine_type, cpu_num=cpu_num, memory_num=memory_num)
        models.Asset.objects.create(host_machine=host_machine, host_name=new_name, host_ip=new_ip,
                                    host_item=machine_type, host_cpu=cpu_num, host_memory=memory_num)

        data_dict['status'] = True
        data_dict['message'] = new_ip

        ret = HttpResponse(json.dumps(data_dict))
        # 设置一个cookie值 引导前端进度条执行
        ret.set_cookie('mess', '200', max_age=5)
        return ret

    def exec_task(self, host_machine, host_name, new_ip, cpu_num, memory_num, br_name, new_gateway, template_mirror):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_machine, port=22, username='root', key_filename=kvm_config.ssh_key_file, timeout=kvm_config.ssh_timeout)
        stdin, stdout, stderr = ssh.exec_command('ls')
        result = stdout.read()
        print(result)

        # 查询数据库中的镜像名称
        template_mirror = kvm_config.kvm_template_dir + template_mirror + '.qcow2'
        # template_mirror = kvm_config.CentOS_6[machine_type]
        # system_version = template_mirror[20]
        # print(system_version)
        new_mirror = kvm_config.kvm_qcow_dir + host_name + '.qcow2'

        # 1、拷贝镜像文件
        # cmd = 'cp %s %s' % (template_mirror, new_mirror)
        cmd = "ssh root@%s 'cp %s %s'" % (host_machine, template_mirror, new_mirror)
        # ssh.exec_command(cmd)
        os.system(cmd)
        print(cmd)

        # 2、新建并修改xml文件
        new_xml_path = self.change_cpu_memory(host_name, cpu_num, memory_num, new_mirror, br_name)
        cmd = 'scp %s root@%s:%s' % (new_xml_path, host_machine, kvm_config.kvm_xml_dir)
        os.system(cmd)
        print(cmd)

        # 3、define虚拟机
        xml_file = '/opt/xml/' + host_name + '.xml'
        # cmd = 'virsh define %s' % xml_file
        # ssh.exec_command(cmd)
        cmd = "ssh root@%s 'virsh define %s'" % (host_machine, xml_file)
        print(cmd)
        os.system(cmd)

        # 4、修改网卡配置文件
        cmd = "ssh root@%s 'mkdir /opt/data/%s && \
        cp /opt/data/ifcfg-eth0 /opt/data/%s/ && \
        cp /opt/data/70-persistent-net.rules /opt/data/%s/ && \
        cp /opt/data/network /opt/data/%s/'" % (host_machine, host_name, host_name, host_name, host_name)
        print(cmd)
        os.system(cmd)

        # cmd = 'mkdir /opt/data/%s' % host_name
        # ssh.exec_command(cmd)
        # print(cmd)
        # cmd = 'cp /opt/data/ifcfg-eth0 /opt/data/%s/' % host_name
        # ssh.exec_command(cmd)
        # print(cmd)
        # cmd = 'cp /opt/data/70-persistent-net.rules /opt/data/%s/' % host_name
        # ssh.exec_command(cmd)
        # print(cmd)
        # cmd = 'cp /opt/data/network /opt/data/%s/' % host_name
        # ssh.exec_command(cmd)
        # print(cmd)
        # time.sleep(2)
        cmd_str = "sed -i 's#%s#%s#g' /opt/data/%s/ifcfg-eth0 && \
               sed -i 's#%s#%s#g' /opt/data/%s/ifcfg-eth0 && \
               sed -i 's#%s#%s#g' /opt/data/%s/network " % (kvm_config.kvm_template_ip, new_ip, host_name,
                                                            '192.168.31.253', new_gateway, host_name,
                                                            kvm_config.kvm_template_hostname, host_name, host_name)
        # stdin, stdout, stderr = ssh.exec_command(cmd)
        # result = stdout.read()
        cmd = "ssh root@%s '%s'" % (host_machine, cmd_str)
        os.system(cmd)
        print(cmd)

        cmd = "ssh root@%s 'virt-copy-in -d %s /opt/data/%s/ifcfg-eth0 /etc/sysconfig/network-scripts/'" % (host_machine, host_name, host_name)
        print(cmd)
        os.system(cmd)

        # cmd = "virt-copy-in -d %s /opt/data/%s/70-persistent-net.rules /etc/udev/rules.d/ && \
        #        virt-copy-in -d %s /opt/data/%s/network /etc/sysconfig/ && \
        #        virsh start %s" % (host_name, host_name, host_name, host_name, host_name)
        # print(cmd)

        cmd = "ssh root@%s 'virt-copy-in -d %s /opt/data/%s/70-persistent-net.rules /etc/udev/rules.d/'" % (host_machine, host_name, host_name)
        print(cmd)
        os.system(cmd)

        cmd = "ssh root@%s 'virt-copy-in -d %s /opt/data/%s/network /etc/sysconfig/'" % (host_machine, host_name, host_name)
        print(cmd)
        os.system(cmd)

        cmd = "ssh root@%s 'virsh start %s'" % (host_machine, host_name)
        print(cmd)
        os.system(cmd)

        # 5、启动虚拟机
        # cmd = 'virsh start %s' % host_name
        # stdin, stdout, stderr = ssh.exec_command(cmd)
        # result = stdout.read()
        # print(result)
        ssh.close()

    def change_cpu_memory(self, host_name, new_cpu, new_memory,  new_mirror, br_name):
        """
        修改KVM模版xml文件 定义新主机
        :param host_name:
        :param new_cpu:
        :param new_memory:
        :param new_mirror:
        :param br_name:
        :return:
        """
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
        host_name = obj[0].host_name
        host_machine = obj[0].mudroom_host
        host_ip = obj[0].host_ip
        print(host_del_id, host_name, host_machine)

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

        # 在总资产表中删除主机
        models.Asset.objects.filter(host_ip=host_ip).delete()

    def change_host_name(self, host_id, host_name):
        """
        修改主机名
        :param host_id:
        :param host_name:
        :return:
        """
        models.VirtualMachines.objects.filter(id=host_id).update(host_name=host_name)
        obj = models.VirtualMachines.objects.filter(id=host_id)
        host_ip = obj[0].host_ip

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_ip, port=22, username='root', password='xinxindai318', timeout=kvm_config.ssh_timeout)

        # 开始更新主机名
        str_host = host_ip + '    ' + host_name
        cmd = "hostname %s && echo %s > /etc/hostname && \
                    sed -i s/%s.*/%s/g /etc/hosts && \
                    sed -i s/HOSTNAME=.*/HOSTNAME=%s/g /etc/sysconfig/network && \
                    service zabbix_agentd restart" % (host_name, host_name, host_ip, str_host, host_name)
        ssh.exec_command(cmd)
        cmd = "service rsyslog restart &"
        ssh.exec_command(cmd)

    def turn_on_off_template(self, template_id, template_status):
        """
        开启或者关闭模版机 模版机有对应IP方便修改
        :param template_id:
        :param template_status:
        :return:
        """
        obj = models.MachineType.objects.filter(id=template_id).first()
        template_host = obj.machine_host
        template_name = obj.machine_name

        if template_status == 'true':
            cmd = "ssh root@%s 'virsh start %s'" % (template_host, template_name)
            print(cmd)
            os.system(cmd)
        else:
            cmd = "ssh root@%s 'virsh destroy %s'" % (template_host, template_name)
            print(cmd)
            os.system(cmd)

    def add_new_mirror(self, mirror_id, mirror_name, mirror_ip):
        """
        自定义镜像文件
        :param mirror_id:
        :param mirror_name:
        :param mirror_ip:
        :return:
        """
        obj = models.VirtualMachines.objects.filter(id=mirror_id).first()
        host = obj.mudroom_host
        old_ip = obj.host_ip
        old_name = '%s-kvm-vhost-%s-%s.%s' % (kvm_config.kvm_addr, old_ip.split('.')[-2], old_ip.split('.')[-1], kvm_config.kvm_str)
        old_mirror = kvm_config.kvm_qcow_dir + old_name + '.qcow2'
        new_mirror = kvm_config.kvm_template_dir + mirror_name + '.qcow2'

        new_name = '%s-kvm-vhost-%s-%s.%s' % (kvm_config.kvm_addr, mirror_ip.split('.')[-2], mirror_ip.split('.')[-1], kvm_config.kvm_str)

        new_gateway = mirror_ip.split('.')
        new_gateway = new_gateway[0] + '.' + new_gateway[1] + '.' + new_gateway[2] + '.' + '253'

        # 创建数据库
        machine_type_obj = models.MachineType(machine_type=mirror_name, machine_ip=mirror_ip, machine_host=host, machine_name=new_name)
        machine_type_obj.save()

        template_mirror_obj = models.MachineType.objects.filter(id=machine_type_obj.id).first()
        template_mirror = template_mirror_obj.machine_type

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=22, username='root', key_filename=kvm_config.ssh_key_file,
                    timeout=kvm_config.ssh_timeout)
        stdin, stdout, stderr = ssh.exec_command('ip addr | grep %s' % host)
        br_name = stdout.read()
        br_name = str(br_name, encoding='utf-8').split(' ')[-1].split('\n')[0]
        cmd = "cp %s %s" % (old_mirror, new_mirror)
        ssh.exec_command(cmd)
        print(cmd)
        ssh.close()

        p = Process(target=self.exec_task,
                    args=(host, new_name, mirror_ip, 2, 2, br_name, new_gateway, template_mirror))
        p.start()

        models.VirtualMachines.objects.create(mudroom_host=host, host_name=new_name, host_ip=mirror_ip,
                                              machine_type_id=machine_type_obj.id, cpu_num=2, memory_num=2)
        models.Asset.objects.create(host_machine=host, host_name=new_name, host_ip=mirror_ip,
                                    host_item=mirror_name, host_cpu=2, host_memory=2)

        data_dict['status'] = True
        data_dict['message'] = "ok"

        ret = HttpResponse(json.dumps(data_dict))
        return ret

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