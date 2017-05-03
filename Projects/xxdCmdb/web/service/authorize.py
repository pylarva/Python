#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import re
import time
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict
from utils.hostname import change_host_name
from multiprocessing import Process
from .base import BaseServiceList
from web.service.mail import send_mail
from conf import mail_config


class Asset(BaseServiceList):
    def __init__(self):
        condition_config = [
            {'name': 'ip', 'text': 'IP', 'condition_type': 'input'},
            {'name': 'username', 'text': '用户名', 'condition_type': 'input'},
            {'name': 'rank', 'text': '权限', 'condition_type': 'select', 'global_name': 'rank_list'},
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
                'q': 'username',
                'title': "用户名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@username'}},
                'attr': {}
            },
            {
                'q': 'ip',
                'title': "IP",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@ip'}},
                'attr': {}
            },
            {
                'q': 'hostname',
                'title': "主机名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@hostname'}},
                'attr': {}
            },
            {
                'q': 'rank',
                'title': "权限",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@rank_list'}},
                'attr': {}
            },
            {
                'q': 'email',
                'title': "邮箱",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@email'}},
                'attr': {}
            },
            {
                'q': 'ctime',
                'title': "申请时间",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@ctime'}},
                'attr': {}
            },
            {
                'q': 'status',
                'title': "状态",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@rank_status_list'}},
                # 'attr': {'style': 'color:green;border:1px solid red;margin-left: 5px;display: inline-block;'}
                # 绿色 92 184 92  黄色 240 173 87 红色 217 83 79
                # 'attr': {'style': 'display: inline-block; padding: 5px; background-color: rgb(92,184,92)', 'id': 'sss'}
                'attr': {}
            },
            {
                'q': None,
                'title': "审批",
                'display': 1,
                'text': {
                    'content': "<a href='#' onclick=do_pass({nid})>通过</a> | <a href='#' onclick=do_refuse({nid})>拒绝</a>",
                    # 'content': "<a href='/asset-1-{nid}.html'>查看详细</a> | <a href='/edit-asset-{device_type_id}-{nid}.html'>编辑</a>",
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id'}},
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
    def rank_status_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.AuthInfo.auth_rank_status)
        return list(result)

    @property
    def rank_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.AuthInfo.auth_rank_choices)
        return list(result)

    @property
    def idc_list(self):
        values = models.IDC.objects.only('id', 'name', 'floor')
        result = map(lambda x: {'id': x.id, 'name': "%s-%s" % (x.name, x.floor)}, values)
        return list(result)

    @property
    def business_1_list(self):
        values = models.BusinessOne.objects.only('id', 'name')
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
        username = request.GET.get('username', None)
        print(username)
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.assets_condition(request)
            asset_count = models.AuthInfo.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            asset_list = models.AuthInfo.objects.filter(conditions).order_by('-id').extra(select=self.extra_select).values(
                *self.values_list)[page_info.start:page_info.end]
            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(asset_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {
                'rank_status_list': self.rank_status_list,
                'rank_list': self.rank_list,
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
            models.AuthInfo.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def put_assets(request):
        pass

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

    def pass_email(asset_id):
        asset = models.AuthInfo.objects.filter(id=asset_id).all()
        ip = asset[0].ip
        hostname = asset[0].hostname
        username = asset[0].username
        rank = asset[0].get_rank_display()
        email = asset[0].email

        mail_info = '堡垒机权限申请成功'
        mail_str = '''
        申请的堡垒机权限已被管理员审批>>

        【   IP   】: %s

        【 主机名 】：%s

        【申请用户】：%s

        【申请权限】：%s

        --------------

        【查询地址】: http://cmdb.xxd.com/authorizer.html
        ''' % (ip, hostname, username, rank)
        send_mail(email, mail_info, mail_str)
        return True

    @staticmethod
    def post_assets(request):
        response = BaseResponse()

        refuse_id = request.POST.get('refuse_id', None)
        pass_id = request.POST.get('pass_id', None)

        if refuse_id:
            try:
                models.AuthInfo.objects.filter(id=refuse_id).update(status=3)
            except Exception as e:
                response.status = False
                response.message = str(e)
                return response
            response.status = True
            return response

        elif pass_id:
            try:
                models.AuthInfo.objects.filter(id=pass_id).update(status=2)
                # 发送邮件
                # p = Process(target=Asset.pass_email, args=(pass_id,))
                # p.start()
            except Exception as e:
                response.status = False
                response.message = str(e)
                return response
            response.status = True
            return response

        ip = request.POST.get('ip')
        username = request.POST.get('username')
        user_rank = request.POST.get('user_rank')
        email = request.POST.get('email')
        hostname = request.POST.get('hostname')

        ctime = time.strftime("%Y-%m-%d %H:%S")
        mail_subject = '堡垒机权限申请--%s' % username
        mail_content = '''
        新增用户堡垒机权限申请>>

        【   IP   】: %s

        【 主机名 】：%s

        【申请用户】：%s

        【申请时间】：%s

        --------------

        【审批地址】: http://cmdb.xxd.com/authorize.html
        ''' % (ip, hostname, username, ctime)

        if not username:
            response.status = False
            response.message = '请先登陆..'
            return response

        record = models.AuthInfo.objects.filter(username=username, ip=ip).count()
        if record > 0:
            response.status = False
            response.message = '已经申请过该主机权限，如果要变更权限，请先取消已有权限并重新申请...'
            return response
        try:
            models.AuthInfo.objects.create(username=username, ip=ip, rank=user_rank, email=email, hostname=hostname)
            # 发送邮件
            # p = Process(target=send_mail, args=(mail_config.mail_admin, mail_subject, mail_content))
            # p.start()
        except Exception as e:
            response.status = False
            response.message = str(e)
            return response
        response.status = True
        return response


