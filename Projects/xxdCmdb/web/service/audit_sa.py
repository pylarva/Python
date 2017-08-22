#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import re
import time
import os
import threading
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict
from utils.hostname import change_host_name
from .base import BaseServiceList
from utils.auditlog import audit_log
from utils.menu import menu
from conf import jenkins_config
import subprocess



class Asset(BaseServiceList):
    def __init__(self):
        condition_config = [
            {'name': 'id', 'text': '发布ID', 'condition_type': 'input'},
            {'name': 'release_name', 'text': '项目名', 'condition_type': 'select', 'global_name': 'business_2_list'},
        ]
        table_config = [
            {
                'q': 'id',
                'title': "发布ID",
                'display': 1,
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {}
            },
            {
                'q': 'release_id',
                'title': "项目ID",
                'display': 0,
                'text': {'content': "{n}", 'kwargs': {'n': '@release_id'}},
                'attr': {}
            },
            {
                'q': 'release_name_id',
                'title': "项目名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@business_2_list'}},
                'attr': {}
            },
            {
                'q': 'release_env_id',
                'title': "环境",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@business_1_list'}},
                'attr': {}
            },
            {
                'q': 'release_type_id',
                'title': "发布类型",
                'display': 0,
                'text': {'content': "{n}", 'kwargs': {'n': '@@release_type_list'}},
                'attr': {}
            },
            {
                'q': 'apply_user',
                'title': "申请用户",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@apply_user'}},
                'attr': {}
            },
            {
                'q': 'release_git_url',
                'title': "GIT地址",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@release_git_url'}},
                'attr': {}
            },
            {
                'q': 'release_git_branch',
                'title': "分支",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@release_git_branch'}},
                'attr': {}
            },
            {
                'q': 'release_reason',
                'title': "发布说明",
                'display': 0,
                'text': {'content': "{n}", 'kwargs': {'n': '@release_reason'}},
                'attr': {}
            },
            {
                'q': 'release_jdk_version',
                'title': "JDK版本",
                'display': 0,
                'text': {'content': "{n}", 'kwargs': {'n': '@@release_jdk_list'}},
                'attr': {}
            },
            {
                'q': 'release_status',
                'title': "状态",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@release_status_list'}},
                'attr': {}
            },
            {
                'q': 'apply_time',
                'title': "申请时间",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@apply_time'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<i class='fa fa-exclamation-triangle' aria-hidden='true'></i><a href='#' style='text-decoration: none;' onclick='audit_pass({id})'> 审核通过</a> | "
                               "<i class='fa fa-paper-plane' aria-hidden='true'></i><a href='#' onclick='do_release(this, {id})'> 执行发布</a> |"
                               "<a href='#' onclick='get_log({id}, false)'> 日志</a> |"
                               "<a href='/release-{id}.html' target='_blank'> 详细</a>",
                    # 'content': "<a href='/asset-1-{nid}.html'>查看详细</a> | <a href='/edit-asset-{device_type_id}-{nid}.html'>编辑</a>",
                    'kwargs': {'device_type_id': '@device_type_id', 'id': '@id'}},
                'attr': {}
            },
        ]
        # 额外搜索条件
        extra_select = {
            'server_title': 'select hostname from repository_server where repository_server.asset_id=repository_asset.id and repository_asset.device_type_id=1',
            'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        super(Asset, self).__init__(condition_config, table_config, extra_select)

    @property
    def release_status_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.ReleaseTask.release_status_choices)
        return list(result)

    @property
    def device_status_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.device_status_choices)
        return list(result)

    @property
    def release_type_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.ReleaseTask.release_status_choices)
        return list(result)

    @property
    def release_jdk_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.ReleaseTask.jdk_version_choice)
        return list(result)

    @property
    def idc_list(self):
        values = models.IDC.objects.only('id', 'name', 'floor')
        result = map(lambda x: {'id': x.id, 'name': "%s-%s" % (x.name, x.floor)}, values)
        return list(result)

    @property
    def business_1_list(self):
        values = models.BusinessOne.objects.filter().only('id', 'name')
        result = map(lambda x: {'id': x.id, 'name': "%s" % x.name}, values)
        return list(result)

    @property
    def business_2_list(self):
        values = models.BusinessTwo.objects.only('id', 'name')
        result = map(lambda x: {'id': x.id, 'name': "%s" % x.name}, values)
        return list(result)

    @property
    def business_3_list(self):
        values = models.BusinessThree.objects.only('id', 'name')
        result = map(lambda x: {'id': x.id, 'name': "%s" % x.name}, values)
        return list(result)

    @property
    def business_unit_list(self):
        values = models.BusinessUnit.objects.values('id', 'name')
        return list(values)

    @property
    def release_type_list(self):
        values = models.ReleaseType.objects.values('id', 'name')
        return list(values)

    @staticmethod
    def assets_condition(request):
        # 创建权限字典
        # condition_dict = {"business_1":["2","3"],"business_2":["3"],"business_3":["3"]}
        condition_dict = {"business_1": [], "business_2": [], "business_3": [], "host_ip__contains": [], "release_status": []}

        # 开始根据用户名查权限
        username = request.GET.get('username')
        # 查看申请列表时用户只允许查看自己的申请记录
        # condition_dict['apply_user'].append(username)
        condition_dict['release_status'].append('6')
        condition_dict['release_status'].append('7')
        condition_dict['release_status'].append('1')
        condition_dict['release_status'].append('2')
        condition_dict['release_status'].append('3')

        # 如果用户属于管理员组 则不限制查询条件
        obj = models.UserProfile.objects.filter(name=username).first()
        is_admin = obj.group.name
        if is_admin != 'admin':
            # 用户组权限
            # business_one_obj = obj.group.business_one.values('id')
            # for item in business_one_obj:
            #     condition_dict['business_1'].append(str(item['id']))
            business_two_obj = obj.group.business_two.values('id')
            for item in business_two_obj:
                condition_dict['business_2'].append(str(item['id']))
            business_three_obj = obj.group.business_three.values('id')
            for item in business_three_obj:
                condition_dict['business_3'].append(str(item['id']))

            # 自定义权限
            # business_one_m = obj.business_one.values('id')
            # for item in business_one_m:
            #     condition_dict['business_1'].append(str(item['id']))
            business_two_m = obj.business_one.values('id')
            for item in business_two_m:
                condition_dict['business_2'].append(str(item['id']))
            business_three_m = obj.business_three.values('id')
            for item in business_three_m:
                condition_dict['business_3'].append(str(item['id']))

            # 如果用户从前端提交查询条件 需要覆盖condition里面对应business_1 2 3 条件
            con_str = request.GET.get('condition', None)
            if con_str != "{}":
                con_dicts = json.loads(con_str)
                con_dicts = dict(con_dicts)
                print('-----', con_dicts, type(con_dicts))

                if con_dicts.get('business_1'):
                    condition_dict['business_1'] = []
                    for item in con_dicts['business_1']:
                        condition_dict['business_1'].append(item)

                if con_dicts.get('business_2'):
                    condition_dict['business_2'] = []
                    for item in con_dicts['business_2']:
                        condition_dict['business_2'].append(item)

                if con_dicts.get('business_3'):
                    condition_dict['business_3'] = []
                    for item in con_dicts['business_3']:
                        condition_dict['business_3'].append(item)

                if con_dicts.get('host_ip__contains'):
                    condition_dict['host_ip__contains'] = con_dicts.get('host_ip__contains')
        else:
            condition_dict = {}

        # 使用Q进行条件格式化
        con_dict = condition_dict
        con_q = Q()
        for k, v in con_dict.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item))
            con_q.add(temp, 'AND')

        return con_q

    def fetch_assets(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.assets_condition(request)
            asset_count = models.ReleaseTask.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            asset_list = models.ReleaseTask.objects.filter(conditions).order_by('-id').extra(select=self.extra_select).values(
                *self.values_list)[page_info.start:page_info.end]

            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(asset_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {
                'device_status_list': self.device_status_list,
                'release_type_list': self.release_type_list,
                'release_status_list': self.release_status_list,
                'idc_list': self.idc_list,
                'business_unit_list': self.business_unit_list,
                'business_1_list': self.business_1_list,
                'business_2_list': self.business_2_list,
                'business_3_list': self.business_3_list,
                'release_jdk_list': self.release_jdk_list
            }
            ret['menu'] = menu(request)
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)

        return response

    @staticmethod
    def delete_assets(request):
        response = BaseResponse()
        try:
            delete_dict = QueryDict(request.body, encoding='utf-8')
            id_list = delete_dict.getlist('id_list')
            status = models.ReleaseTask.objects.filter(id=id_list[0]).first().release_status
            if status != 4:
                response.status = False
                response.message = '非待审核状态不能删除'
            else:
                models.ReleaseTask.objects.filter(id__in=id_list).delete()
                response.message = '删除成功'
        except Exception as e:
            response.status = True
            # response.message = str(e)
        return response

    @staticmethod
    def put_assets(request):
        response = BaseResponse()
        response.status = True
        return response

    @staticmethod
    def assets_detail(device_type_id, asset_id):

        response = BaseResponse()
        try:
            if device_type_id == '1':
                response.data = models.Server.objects.filter(asset_id=asset_id).select_related('asset').first()
            else:
                response.data = models.NetworkDevice.objects.filter(asset_id=asset_id).select_related('asset').first()

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    # @staticmethod
    def post_assets(self, request):
        response = BaseResponse()

        # 运维审核完成后-开始发布
        release_id = request.POST.get('release_id', None)
        if release_id:
            status = models.ReleaseTask.objects.filter(id=release_id).first().release_status
            # 发布任务状态不是 待发布 不允许进行发布
            if status not in [3, 7]:
                response.status = False
                response.message = '待审任务或完成状态不允许执行发布..'
                return response
            # 开始创建发布任务
            else:
                models.ReleaseTask.objects.filter(id=release_id).update(release_status=1)
                self.post_task(release_id)
                audit_log(release_id, '[ %s ] 开始执行发布' % request.session['username'])
                response.status = True
                return response

        # 运维审核流程
        audit_id = request.POST.get('audit_id', None)
        if audit_id:
            user = request.session['username']

            models.ReleaseTask.objects.filter(id=audit_id).update(release_status=7)
            audit_log(audit_id, '[ %s ] SA审核通过' % user)
            audit_log(audit_id, '[ 系统 ] 等待发布..')

            response.status = True
            return response

        # 前端页面请求任务状态
        task_id = request.POST.getlist('task_id', None)
        if task_id:
            task_id_list = task_id
            con_q = Q()
            con_q.connector = 'OR'
            for item in task_id_list:
                con_q.children.append(('id', item))
            obj_list = models.ReleaseTask.objects.filter(con_q).values('id', 'release_status')
            response.data = {'data_list': list(obj_list)}

        response.status = True
        return response

    def post_task(self, release_id):
        """
        审核完成后的发布任务不需要再填写分支 直接发布
        :param release_id:
        :return:
        """

        release_obj = models.ReleaseTask.objects.filter(id=release_id).first()
        # release_type = release_obj.release_type
        release_env_name = release_obj.release_env.name
        release_branch = release_obj.release_git_branch
        release_user = release_obj.apply_user
        project_id = release_obj.release_id

        obj = models.ProjectTask.objects.filter(id=project_id).first()
        release_name = obj.business_2
        pack_cmd = obj.pack_cmd
        static_type = obj.static_type

        release_git_url = obj.git_url
        release_jdk_version = obj.jdk_version
        release_type = obj.project_type_id

        release_business_1 = release_obj.release_env
        release_business_2 = release_obj.release_name
        task_id = release_obj.id

        if release_type == 2:
            pkg_name = "/data/packages/%s/%s/%s/%s.zip" % (release_business_1, release_business_2, release_obj.id,
                                                           jenkins_config.static_pkg_name[release_name])
        else:
            pkg_name = "/data/packages/%s/%s/%s/%s.war" % (release_business_1, release_business_2, release_obj.id,
                                                           release_business_2)

        # 多进程执行连接Jenkins执行
        # p = Process(target=self.JenkinsTask, args=(pkg_name, release_git_url, release_branch, task_id, obj))
        # p.start()

        # 多线程
        t = threading.Thread(target=self.jenkins_task, args=(pkg_name, release_git_url, release_branch, task_id,
                                                             release_name, release_env_name, pack_cmd, release_type,
                                                             release_jdk_version, static_type, release_user))
        t.start()
        return True

    def jenkins_task(self, pkg_name, release_git_url, release_branch, task_id, release_name, release_env, pack_cmd,
                     release_type, jdk_version, static_type, release_user):

        jdk = {'1': '/usr/local/jdk8', '2': '/usr/local/jdk7', '3': '/usr/java/jdk1.6.0_32'}
        static = {'1': '覆盖式', '2': '迭代式'}
        release_types = {'1': 'Tomcat', '2': 'Static'}

        self.log(task_id, '------------------- 开始创建发布任务 -------------------')
        self.log(task_id, '项目名称: %s' % release_name)
        self.log(task_id, '发布类型: %s' % release_types[str(release_type)])
        self.log(task_id, '发布环境: %s 发布分支: %s 发布用户: %s' % (release_env, release_branch, release_user))
        self.log(task_id, 'Java版本: %s 静态资源类型: %s' % (jdk[str(jdk_version)], static[str(static_type)]))
        # self.log(task_id, 'git地址:%s' % release_git_url)
        self.log(task_id, '资源地址: %s' % pkg_name.replace('/data/packages', jenkins_config.pkgUrl))
        self.log(task_id, '-----------------------------------------------------------')

        self.log(task_id, '尝试连接Jenkins...')

        # time.sleep(10)
        # models.ReleaseTask.objects.filter(id=task_id).update(release_status=2)
        # return True

        # 将发布脚本发送到目标机器
        cmd = "/usr/bin/scp -r %s root@%s:/opt/" % (jenkins_config.source_script_path, jenkins_config.host)
        os.system(cmd)

        # 将配置文件发送到目标机器
        cmd = '/usr/bin/scp -r %s root@%s:/opt/' % (jenkins_config.config_path, jenkins_config.host)
        os.system(cmd)

        pack_cmd = '"' + pack_cmd + '"'
        cmd = "python2.6 {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}".format(*[jenkins_config.script_path, pkg_name, task_id,
                                                                              release_git_url, release_branch, release_name,
                                                                              release_env, pack_cmd, jdk_version, release_type, static_type])

        cmd = "ssh root@192.168.31.80 '%s'" % cmd
        print(cmd)
        os.system(cmd)

        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(jenkins_config.host, port=22, username='root', password='xinxindai318', timeout=3)
        # stdin, stdout, stderr = ssh.exec_command(cmd)
        # result = stdout.read()

        obj = models.ReleaseTask.objects.filter(id=task_id).first()
        md5 = obj.release_md5
        print(md5)

        # 发布类型为静态资源
        if release_type == 2:
            if release_env != 'prod':
                nginx_ip_list = jenkins_config.nginx_test_ip_list
            else:
                nginx_ip_list = jenkins_config.nginx_prod_ip_list

            if nginx_ip_list:
                self.log(task_id, '------ 开始发布静态资源 ------')

                num = 1
                self.log(task_id, nginx_ip_list)
                for ip in nginx_ip_list:
                    self.log(task_id, '当前发布第%s台Nginx服务器%s...' % (num, ip))
                    ret = self.nginx_task(ip, release_name, pkg_name, task_id, release_env, static_type, release_branch)
                    if not ret:
                        self.log(task_id, '发布第%s台Nginx服务器%s...【失败】' % (num, ip))
                        self.log(task_id, '终止发布...')
                        models.ReleaseTask.objects.filter(id=task_id).update(release_status=3)
                        return False
                    if release_name == 'apk':
                        self.log(task_id, 'apk项目仅需发布一台nginx服务器...')
                        self.log(task_id, '正在刷新cdn..')

                        cmd = 'cd %s && python2.6 cdn.py Action=RefreshObjectCaches ObjectType=File ObjectPath=%s' % \
                              (os.path.dirname(jenkins_config.source_script_path), jenkins_config.cdn_url_1)
                        self.log(task_id, cmd)
                        ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                               preexec_fn=os.setsid)
                        out, err = ret.communicate()
                        url = str(out, encoding='utf-8')
                        cmd = 'curl %s' % url
                        ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                               preexec_fn=os.setsid)
                        out, err = ret.communicate()

                        cmd = 'cd %s && python2.6 cdn.py Action=RefreshObjectCaches ObjectType=File ObjectPath=%s' % \
                              (os.path.dirname(jenkins_config.source_script_path), jenkins_config.cdn_url_2)
                        self.log(task_id, cmd)
                        ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                               preexec_fn=os.setsid)
                        out, err = ret.communicate()
                        url = str(out, encoding='utf-8')
                        cmd = 'curl -I %s' % url
                        ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                               preexec_fn=os.setsid)
                        out, err = ret.communicate()

                        break
                    num += 1

                models.ReleaseTask.objects.filter(id=task_id).update(release_status=2)
                self.log(task_id, '发布成功结束！')
                return True
            else:
                models.ReleaseTask.objects.filter(id=task_id).update(release_status=3)
                self.log(task_id, '未配置nginx服务器地址..')
                return False

        if md5:
            self.log(task_id, '生成资源md5...检查是否需要发布静态资源')
            # 打包成功后查找业务线节点机器 环境 + 业务线
            release_obj = models.ReleaseTask.objects.filter(id=task_id).first()
            business_1 = release_obj.release_env
            business_2 = release_obj.release_name
            md5sum = release_obj.release_md5
            release_type = release_obj.release_type
            count = models.Asset.objects.filter(business_1=business_1, business_2=business_2).count()
            values = models.Asset.objects.filter(business_1=business_1, business_2=business_2).only('id', 'host_ip')

            # 发布 front和 webapp 的静态资源
            name = str(release_name)
            if name in jenkins_config.static_nginx_dict:
                self.log(task_id, '----- 向Nginx发布static静态资源 -----')
                num = 1
                if release_env != 'prod':
                    nginx_ip_list = jenkins_config.nginx_test_ip_list
                else:
                    nginx_ip_list = jenkins_config.nginx_prod_ip_list

                result = True
                if nginx_ip_list:
                    for ip in nginx_ip_list:
                        self.log(task_id, '当前发布第%s台Nginx服务器%s...' % (num, ip))
                        ret = self.nginx_task(ip, release_name, pkg_name, task_id, release_env, static_type, release_branch)
                        if not ret:
                            self.log(task_id, '发布第%s台Nginx服务器%s...【失败】' % (num, ip))
                            self.log(task_id, '终止发布...')
                            models.ReleaseTask.objects.filter(id=task_id).update(release_status=3)
                            result = False
                            break
                        num += 1
                else:
                    self.log(task_id, '未配置nginx服务器地址..')

                if not result:
                    self.log(task_id, '发布失败！')
                    return False

            self.log(task_id, '----- 共需发布【%s】台节点服务器 -------' % count)
            num = 1
            result = True
            for item in values:
                print(item.host_ip)
                self.log(task_id, '当前发布第%s台%s...' % (num, item.host_ip))
                # 目标机开始执行发布脚本
                ret = self.shell_task(item.host_ip, pkg_name, md5sum, task_id, release_type, business_2)
                if not ret:
                    self.log(task_id, '当前发布第%s台%s...【失败】' % (num, item.host_ip))
                    self.log(task_id, '终止发布...')
                    models.ReleaseTask.objects.filter(id=task_id).update(release_status=3)
                    result = False
                    break
                num += 1

            if result:
                if release_type == 1:
                    self.log(task_id, 'Java start success...')
                self.log(task_id, '发布成功结束！')
                audit_log(task_id, '[ 系统 ] 发布成功结束！')
                models.ReleaseTask.objects.filter(id=task_id).update(release_status=2)
            else:
                self.log(task_id, '发布失败！')
                models.ReleaseTask.objects.filter(id=task_id).update(release_status=3)

        else:
            # ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
            #                        preexec_fn=os.setsid)
            # out, err = ret.communicate()
            # err = str(err, encoding='utf-8')
            # self.log(task_id, err)
            # self.log(task_id, '......拉取代码失败')
            self.log(task_id, '发布终止！')
            models.ReleaseTask.objects.filter(id=task_id).update(release_status=3)

    def log(self, task_id, msg):
        """
        记录日志
        :param task_id:
        :param msg:
        :return:
        """
        models.ReleaseLog.objects.create(release_id=task_id, release_msg=msg)

    def shell_task(self, ip, pkgUrl, md5sum, taskId, serviceType, name):
        """
        连接发布目标机开始执行发布脚本
        :return:
        """
        pkgUrl = pkgUrl.replace('/data/packages', jenkins_config.pkgUrl)
        cmd = "scp %s root@%s:/opt/" % (jenkins_config.source_script_path, ip)
        os.system(cmd)

        # 将配置文件发送到目标机器
        cmd = '/usr/bin/scp -r %s root@%s:/opt/' % (jenkins_config.config_path, ip)
        os.system(cmd)

        cmd = "ssh root@%s 'pip install requests'" % ip
        os.system(cmd)

        cmd = "ssh root@%s 'python2.6 %s %s %s %s %s %s'" % (ip, jenkins_config.script_path, pkgUrl, md5sum, taskId, serviceType, name)
        # 脚本执行过程中 会陆续上传执行日志
        ret = os.system(cmd)
        if ret:
            self.log(taskId, '错误代码...%s' % ret)
            print(ret)
            return False
        # print(out, err)
        print(ret)
        return True

    def nginx_task(self, ip, name, pkgUrl, taskId, env, static_type, branch):
        pkgUrl = pkgUrl.replace('/data/packages', jenkins_config.pkgUrl)

        if name in jenkins_config.static_nginx_dict:
            pkgUrl = '%s/%s' % (os.path.dirname(pkgUrl), 'static.zip')

        cmd = "scp %s root@%s:/opt/" % (jenkins_config.source_script_path, ip)
        os.system(cmd)

        cmd = "ssh root@%s 'pip install requests'" % ip
        os.system(cmd)

        cmd = "ssh root@%s 'python2.6 %s %s %s %s %s %s %s'" % (ip, jenkins_config.script_path, name, pkgUrl, taskId, env,
                                                                static_type, branch)
        self.log(taskId, '%s' % cmd)
        print(cmd)
        ret = os.system(cmd)
        if ret:
            self.log(taskId, '发布静态资源错误, 代码...%s' % ret)
            return False
        return True

