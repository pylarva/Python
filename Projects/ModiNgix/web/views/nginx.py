# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import subprocess
from web import models
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse


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
            self.exec_cmd(cmd)
            self.exec_cmd('chmod 777 %s' % file)

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
            print(name)
            name_del = 'still_range %s' % name.split(',')[1]
            print(name_del)
            file = '/opt/%s' % os.path.basename(path)

            # 免密钥拉取配置文件
            if os.path.exists(file):
                cmd = 'rm -fr %s' % file
                self.exec_cmd(cmd)
            cmd = 'scp root@%s:%s /opt/' % (ip, path)
            self.exec_cmd(cmd)
            self.exec_cmd('chmod 777 %s' % file)

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
            self.exec_cmd(cmd)

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

        new_str = 'still_range %s%s%sT%s%s%s %ss;' % (year, month, day, hour, minute, second, s_time)
        print(new_str)
        file = '/opt/%s' % os.path.basename(path)
        # 免密钥拉取配置文件
        if os.path.exists(file):
            cmd = 'rm -fr %s' % file
            self.exec_cmd(cmd)
        cmd = 'scp root@%s:%s /opt/' % (ip, path)
        self.exec_cmd(cmd)
        self.exec_cmd('chmod 777 %s' % file)

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
        self.exec_cmd(cmd)

        return JsonResponse(response.__dict__)

    def exec_cmd(self, cmd_shell):
        """
        执行远程命令
        :param cmd_shell:
        :return:
        """
        # print(cmd_shell)
        try:
            ret = subprocess.Popen(cmd_shell, stdin=subprocess.PIPE, shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            err = ret.stderr.read()
            if err:
                print('--------', err)
        except Exception as e:
            print(e)
        return True
