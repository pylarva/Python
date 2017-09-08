#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import re
import os
import time
import random
import threading
import hashlib
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict
from utils.hostname import change_host_name
from .base import BaseServiceList
from utils.mail import send_mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from conf import mail_config


class Asset(BaseServiceList):
    def __init__(self):
        condition_config = [
            {'name': 'name', 'text': '用户', 'condition_type': 'input'},
        ]
        table_config = [
            {
                'q': 'id',
                'title': "ID",
                'display': 0,
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {}
            },
            {
                'q': 'name',
                'title': "用户名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {}
            },
            {
                'q': 'active',
                'title': "状态",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@active_status_list'}},
                'attr': {}
            },
            {
                'q': 'register_time',
                'title': "注册时间",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@register_time'}},
                'attr': {'name': 'register_time', 'id': '@register_time', 'original': '@register_time',
                         'edit-enable': 'true',
                         'edit-type': 'input'}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<i class='fa fa-pencil' aria-hidden='true'></i> <a href='#' onclick='change_pwd({nid})'>更改密码</a> |"
                               " <i class='fa fa-lock' aria-hidden='true'></i><a href='#' onclick='cancle_account({nid})'> 账号冻结</a>",
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id'}},
                'attr': {'style': 'width: 200px'}
            },
        ]
        # 额外搜索条件
        extra_select = {
            'server_title': 'select hostname from repository_server where repository_server.asset_id=repository_asset.id and repository_asset.device_type_id=1',
            'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        super(Asset, self).__init__(condition_config, table_config, extra_select)

    @property
    def device_status_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.device_status_choices)
        return list(result)

    @property
    def device_type_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.device_type_choices)
        return list(result)

    @property
    def active_status_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.VpnAccount.active_status)
        return list(result)

    @property
    def idc_list(self):
        values = models.IDC.objects.only('id', 'name', 'floor')
        result = map(lambda x: {'id': x.id, 'name': "%s-%s" % (x.name, x.floor)}, values)
        return list(result)

    @property
    def business_1_list(self):
        # # 基于用户session用户名来查用户权限
        # username = request.GET.get('username')
        #
        # # 1、业务1权限
        # business_one_condition = Q()
        #
        # #    先将用户组中的权限添加进condition
        # obj = models.UserProfile.objects.filter(name=username).first()
        # business_one_obj = obj.group.business_one.all()
        # business_one_condition.connector = 'OR'
        # for item in business_one_obj:
        #     print(item)
        #     item = str(item)
        #     business_one_condition.children.append(('name', item))
        #
        # #    再将自定义的业务权限添加进condition
        # business_one_modification = obj.business_one.all()
        # for item in business_one_modification:
        #     print(item)
        #     item = str(item)
        #     business_one_condition.children.append(('name', item))
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

    @staticmethod
    def assets_condition(request):
        con_str = request.GET.get('condition', None)
        print(con_str)
        if not con_str:
            con_dict = {}
        else:
            con_dict = json.loads(con_str)

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
            asset_count = models.VpnAccount.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            asset_list = models.VpnAccount.objects.filter(conditions).extra(select=self.extra_select).values(
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
                'active_status_list': self.active_status_list,
                'device_type_list': self.device_type_list,
                'idc_list': self.idc_list,
                'business_unit_list': self.business_unit_list,
                'business_1_list': self.business_1_list,
                'business_2_list': self.business_2_list,
                'business_3_list': self.business_3_list
            }
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
            models.VpnAccount.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    # @staticmethod
    def put_assets(self, request):
        """
        添加新的VPN账号
        :param request:
        :return:
        """
        response = BaseResponse()

        # 注销冻结\解封
        cancle_id = request.POST.get('cancle_id', None)
        if cancle_id:
            try:
                current_statue = models.VpnAccount.objects.filter(id=cancle_id).first().active
                if current_statue == 1:
                    models.VpnAccount.objects.filter(id=cancle_id).update(active=2)
                elif current_statue == 2:
                    models.VpnAccount.objects.filter(id=cancle_id).update(active=1)
                response.status = True
                response.message = '更新成功！'
            except Exception as e:
                response.status = False
                response.message = '%s' % e
            return response

        # 更新密码
        new_pwd = request.POST.get('new_pwd', None)
        if new_pwd:
            new_id = request.POST.get('id', None)
            try:
                cmd = "mysql -uroot -proot -e \"update xxdcmdb.repository_vpnaccount set " \
                      "password=PASSWORD('%s') where id=%s;\"" % (new_pwd, new_id)
                os.system(cmd)
                response.status = True
                response.message = '更新成功！'
            except Exception as e:
                response.status = False
                response.message = '%s' % e
            return response

        new_name = request.POST.get('new_name', None)
        name_exist = models.VpnAccount.objects.filter(name=new_name).count()
        if name_exist:
            response.status = False
            response.message = '用户名已经存在..'
            return response

        # 随机生成一个8位密码
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
        sa = []
        for i in range(8):
            sa.append(random.choice(seed))
        salt = ''.join(sa)
        # obj = hashlib.md5()
        # obj.update(bytes(salt, encoding='utf-8'))
        # md5_pwd = obj.hexdigest()

        # 先手动插入一条PASSWORD数据
        r_time = time.strftime('%Y-%m-%d')
        cmd = "mysql -uroot -proot -h%s -e \"insert into xxdcmdb.repository_vpnaccount " \
              "values('%s', '', '%s', PASSWORD('%s'), 1);\"" % (mail_config.openvpn_db, r_time, new_name, salt)
        os.system(cmd)
        # models.VpnAccount.objects.create(name=new_name, password=md5_pwd, active=1, register_time=r_time)

        # 发送邮件
        mail_to = '%s@xinxindai.com' % new_name
        subject = '【VPN账号开通成功】'
        content = '账户: %s \n密码: %s \n\n 客户端下载: %s' % (new_name, salt, mail_config.openvpn_url)
        t = threading.Thread(target=send_mail, args=(mail_to, subject, content))
        t.start()
        response.status = True
        response.message = 'vpn账户开通成功！\n 账户: %s \n密码: %s' % (new_name, salt)
        return response

    @staticmethod
    def assets_detail(nid, device_type_id):

        response = BaseResponse()
        print(device_type_id, nid)
        try:
            if device_type_id == 1:
                response.data = models.DellServer.objects.filter(asset_id=nid).first()
            else:
                response.data = models.NetWork.objects.filter(asset=nid).first()

        except Exception as e:
            response.status = False
            response.message = str(e)
        response.status = True

        return response

    def send_mail(self, mail_to, subject, content):
        mail_host = 'smtp.partner.outlook.cn'
        mail_port = 587
        mail_user = 'monitor@xinxindai.com'
        mail_pass = 'Yhblsqt520'
        mail_postfix = 'xinxindai.com'

        me = mail_user
        # msg = MIMEText(content)
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = me
        msg['to'] = mail_host
        att1 = MIMEText(open('/opt/openvpn.tgz', 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="hahahha.zip"'
        msg.attach(att1)

        try:
            smtp = smtplib.SMTP()
            smtp.connect(mail_host, mail_port)
            smtp.starttls()
            smtp.login(mail_user, mail_pass)
            smtp.sendmail(me, mail_to, msg.as_string())
            smtp.close()
            print('Email send ok...')
        except Exception as e:
            senderr = str(e)
            print(senderr)
            sendstatus = False
        return True


