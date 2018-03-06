# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import paramiko
import subprocess
from web import models
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from conf import config
from crontab import CronTab


class BaseResponse(object):
    def __init__(self):
        self.status = True
        self.message = None
        self.data = None
        self.error = None


class IndexView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class NginxView(View):
    def get(self, request, *args, **kwargs):
        data = models.NginxHost.objects.all()
        ip = request.GET.get('ip')
        if ip:
            # cmd = 'ssh root@%s ls' % ip
            # ret = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True,
            #                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            # if ret.stderr.read():
            #     print(ret.stderr.read())
            path = request.GET.get('path')
            response = BaseResponse()
            # 获取屏蔽记录

            # 免密钥拉取配置文件
            file = '/opt/%s' % os.path.basename(path)
            if os.path.exists(file):
                cmd = 'rm -fr %s' % file
                self.exec_cmd(cmd)
            cmd = 'scp root@%s:%s /opt/' % (ip, path)
            status, err = self.exec_cmd(cmd)
            if not status:
                response.status = False
                response.error = err
                return JsonResponse(response.__dict__)
            status, err = self.exec_cmd('chmod 777 %s' % file)
            if not status:
                response.status = False
                response.error = err
                return JsonResponse(response.__dict__)
            # 读取文件
            data_list = []
            with open(file, 'r') as f:
                for line in f:
                    if re.match('\s+still_range', line):
                        data_list.append(line.split())
            response.data = data_list
            response.status = True
            return JsonResponse(response.__dict__)
        return render(request, 'nginx.html', {'data': data})

    def post(self, request, *args, **kwargs):
        response = BaseResponse()
        response.status = True

        is_del = request.POST.get('is_del')
        if is_del:
            ip = request.POST.get('ip')
            path = request.POST.get('path')
            name = request.POST.get('name')
            reload_cmd = request.POST.get('cmd')
            print(name)
            name_del = 'still_range %s' % name.split(',')[1]
            print(name_del)
            file = '/opt/%s' % os.path.basename(path)

            # 免密钥拉取配置文件
            if os.path.exists(file):
                cmd = 'rm -fr %s' % file
                self.exec_cmd(cmd)
            cmd = 'scp root@%s:%s /opt/' % (ip, path)
            status, err = self.exec_cmd(cmd)
            if not status:
                response.status = False
                response.error = err
                return JsonResponse(response.__dict__)
            status, err = self.exec_cmd('chmod 777 %s' % file)
            if not status:
                response.status = False
                response.error = err
                return JsonResponse(response.__dict__)

            # 修改文件
            new_file = '/opt/newfile.conf'
            if not os.path.exists(new_file):
                os.system('touch %s' % new_file)
            with open(file, 'r') as readfile, open(new_file, 'w') as writefile:
                for line in readfile:
                    if re.match('\s+%s' % name_del, line):
                        pass
                    else:
                        writefile.write(line)

            # 拷贝新文件到nginx机器
            cmd = 'scp /opt/newfile.conf root@%s:%s' % (ip, path)
            status, err = self.exec_cmd(cmd)
            if not status:
                response.status = False
                response.error = err
                return JsonResponse(response.__dict__)

            # 重启nginx
            cmd = 'ssh root@%s %s' % (ip, reload_cmd)
            status, err = self.exec_cmd(cmd)
            if not status:
                response.error = err
                response.status = False
                return JsonResponse(response.__dict__)

            return JsonResponse(response.__dict__)

        ip = request.POST.get('ip')
        path = request.POST.get('path')
        year = request.POST.get('year')
        month = request.POST.get('month')
        day = request.POST.get('day')
        hour = request.POST.get('hour')
        minute = request.POST.get('minute')
        second = request.POST.get('second')
        s_time = request.POST.get('time')
        reload_cmd = request.POST.get('cmd')

        new_str = 'still_range %s%s%sT%s%s%s %ss;' % (year, month, day, hour, minute, second, s_time)
        print(new_str)
        file = '/opt/%s' % os.path.basename(path)
        # 免密钥拉取配置文件
        if os.path.exists(file):
            cmd = 'rm -fr %s' % file
            self.exec_cmd(cmd)
        cmd = 'scp root@%s:%s /opt/' % (ip, path)
        status, err = self.exec_cmd(cmd)
        if not status:
            response.status = False
            response.error = err
            return JsonResponse(response.__dict__)

        status, err = self.exec_cmd('chmod 777 %s' % file)
        if not status:
            response.status = False
            response.error = err
            return JsonResponse(response.__dict__)

        # 修改文件
        new_file = '/opt/newfile.conf'
        if not os.path.exists(new_file):
            os.system('touch %s' % new_file)
        with open(file, 'r') as readfile, open(new_file, 'w') as writefile:
            for line in readfile:
                if re.match('\s+timeshift_segments_per_playlist', line):
                    writefile.write(line)
                    writefile.write('    %s\n' % new_str)
                else:
                    writefile.write(line)

        # 拷贝新文件到nginx机器
        cmd = 'scp /opt/newfile.conf root@%s:%s' % (ip, path)
        status, err = self.exec_cmd(cmd)
        if not status:
            response.status = False
            response.error = err
            return JsonResponse(response.__dict__)

        # 重启nginx
        cmd = 'ssh root@%s %s' % (ip, reload_cmd)
        status, err = self.exec_cmd(cmd)
        if not status:
            response.error = err
            response.status = False
            return JsonResponse(response.__dict__)

        return JsonResponse(response.__dict__)

    def exec_cmd(self, cmd_shell):
        """
        执行远程命令
        :param cmd_shell:
        :return:
        """
        print(cmd_shell)
        try:
            ret = subprocess.Popen(cmd_shell, stdin=subprocess.PIPE, shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            err = ret.stderr.read()
            if err:
                print('--------', err)
                return 0, err
        except Exception as e:
            print(e)
        return 1, 1


class CrontabView(View):

    def get(self, request):
        host_ip = config.crontab_host
        ip = request.GET.get('ip')
        if ip:
            # cmd = 'ssh root@%s ls' % ip
            # ret = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True,
            #                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            # if ret.stderr.read():
            #     print(ret.stderr.read())
            # path = request.GET.get('path')
            response = BaseResponse()
            path = '/var/spool/cron/root'

            # 免密钥拉取配置文件
            file = '/opt/%s' % os.path.basename(path)
            if os.path.exists(file):
                cmd = 'rm -fr %s' % file
                self.exec_cmd(cmd)
            cmd = 'scp root@%s:%s /opt/' % (ip, path)
            status, err = self.exec_cmd(cmd)
            if not status:
                response.status = False
                response.error = err
                return JsonResponse(response.__dict__)
            status, err = self.exec_cmd('chmod 777 %s' % file)
            if not status:
                response.status = False
                response.error = err
                return JsonResponse(response.__dict__)
            # 读取文件
            data_list = []
            with open(file, 'r') as f:
                for line in f:
                    data_list.append(line.split())
            response.data = data_list
            response.status = True
            return JsonResponse(response.__dict__)
        return render(request, 'crontab.html', {'host_ip': host_ip})

    def post(self, request):
        response = BaseResponse()
        response.status = True
        path = '/var/spool/cron/root'

        is_del = request.POST.get('is_del')
        if is_del:
            ip = request.POST.get('ip')
            name = request.POST.get('name')
            print(name)

            name_del = name.split(',')[-3]
            print(name_del)

            file = '/opt/%s' % os.path.basename(path)

            # 免密钥拉取配置文件
            if os.path.exists(file):
                cmd = 'rm -fr %s' % file
                self.exec_cmd(cmd)
            cmd = 'scp root@%s:%s /opt/' % (ip, path)
            status, err = self.exec_cmd(cmd)
            if not status:
                response.status = False
                response.error = err
                return JsonResponse(response.__dict__)
            status, err = self.exec_cmd('chmod 777 %s' % file)
            if not status:
                response.status = False
                response.error = err
                return JsonResponse(response.__dict__)

            # 修改文件
            new_file = '/opt/newfile.conf'
            if not os.path.exists(new_file):
                os.system('touch %s' % new_file)
            with open(file, 'r') as readfile, open(new_file, 'w') as writefile:
                for line in readfile:
                    if re.search('%s' % name_del, line):
                        pass
                        print(66666)
                    else:
                        print(line)
                        writefile.write(line)

            # 拷贝新文件到nginx机器
            cmd = 'scp /opt/newfile.conf root@%s:%s' % (ip, path)
            status, err = self.exec_cmd(cmd)
            if not status:
                response.status = False
                response.error = err
                return JsonResponse(response.__dict__)

            return JsonResponse(response.__dict__)

        ip = request.POST.get('ip')
        crontab_time = request.POST.get('crontab_time')
        crontab_1 = request.POST.get('crontab_1')
        crontab_2 = request.POST.get('crontab_2')

        month = crontab_time[4:6]
        day = crontab_time[6:8]

        new_str = config.crontab_cmd.replace('AA', day).replace('BB', month).replace('CC', crontab_time).\
            replace('DD', crontab_1).replace('EE', crontab_2)
        print(new_str)

        file = '/opt/%s' % os.path.basename(path)
        # 免密钥拉取配置文件
        if os.path.exists(file):
            cmd = 'rm -fr %s' % file
            self.exec_cmd(cmd)
        cmd = 'scp root@%s:%s /opt/' % (ip, path)
        status, err = self.exec_cmd(cmd)
        if not status:
            response.status = False
            response.error = err
            return JsonResponse(response.__dict__)

        status, err = self.exec_cmd('chmod 777 %s' % file)
        if not status:
            response.status = False
            response.error = err
            return JsonResponse(response.__dict__)

        # 修改文件
        # new_file = '/opt/newroot.conf'
        # if not os.path.exists(new_file):
        #     os.system('touch %s' % new_file)
        with open(file, "a+") as f:
            f.write("%s\n" % new_str)

        # 拷贝新文件到nginx机器
        cmd = 'scp /opt/root root@%s:%s' % (ip, path)
        status, err = self.exec_cmd(cmd)
        if not status:
            response.status = False
            response.error = err
            return JsonResponse(response.__dict__)
        return JsonResponse(response.__dict__)


    def exec_cmd(self, cmd_shell):
        """
        执行远程命令
        :param cmd_shell:
        :return:
        """
        print(cmd_shell)
        try:
            ret = subprocess.Popen(cmd_shell, stdin=subprocess.PIPE, shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            err = ret.stderr.read()
            if err:
                print('--------', err)
                return 0, err
        except Exception as e:
            print(e)
        return 1, 1
