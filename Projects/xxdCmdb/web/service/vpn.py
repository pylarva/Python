#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import re
import time
import random
import hashlib
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict
from utils.hostname import change_host_name
from .base import BaseServiceList


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
                    'content': "<a href='/asset-{nid}.html' target='_blank'>更改密码</a> |"
                               "<a href='/asset-{nid}.html' target='_blank'> 注销</a>",
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
            models.Asset.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def put_assets(request):
        """
        添加新的VPN账号
        :param request:
        :return:
        """
        response = BaseResponse()
        new_name = request.POST.get('new_name', None)
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
        sa = []
        for i in range(8):
            sa.append(random.choice(seed))
        salt = ''.join(sa)
        obj = hashlib.md5()
        obj.update(bytes(salt, encoding='utf-8'))
        md5_pwd = obj.hexdigest()
        print(md5_pwd)
        r_time = time.strftime('%Y-%m-%d')
        models.VpnAccount.objects.create(name=new_name, password=md5_pwd, active=1, register_time=r_time)

        response.status = True
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


