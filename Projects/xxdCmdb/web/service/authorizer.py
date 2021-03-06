#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import re
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict
from utils.hostname import change_host_name
from .base import BaseServiceList
from utils.menu import menu


class Asset(BaseServiceList):
    def __init__(self):
        condition_config = [
            {'name': 'host_ip', 'text': 'IP', 'condition_type': 'input'},
            {'name': 'business_1', 'text': '业务类型1', 'condition_type': 'select', 'global_name': 'business_1_list'},
            {'name': 'business_2', 'text': '业务类型2', 'condition_type': 'select', 'global_name': 'business_2_list'},
            {'name': 'business_3', 'text': '业务类型3', 'condition_type': 'select', 'global_name': 'business_3_list'},
            {'name': 'host_status', 'text': '资产状态', 'condition_type': 'select',
             'global_name': 'device_status_list'},
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
                'q': 'status',
                'title': "状态",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@device_status_list'}},
                'attr': {'style': 'color:green;'}
            },
            {
                'q': 'email',
                'title': "邮箱",
                'display': 0,
                'text': {'content': "{n}", 'kwargs': {'n': '@email'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<a href='#' onclick=d_record({nid})>取消</a>",
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
    def device_status_list(self):
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
        response = BaseResponse()
        username = request.GET.get('username')
        try:
            ret = {}
            # conditions = self.assets_condition(request)
            asset_count = models.AuthInfo.objects.filter(username=username).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            asset_list = models.AuthInfo.objects.filter(username=username).extra(select=self.extra_select).values(
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
                'rank_list': self.rank_list,
                'idc_list': self.idc_list,
                'business_unit_list': self.business_unit_list,
                'business_1_list': self.business_1_list,
                'business_2_list': self.business_2_list,
                'business_3_list': self.business_3_list
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
            id_list = delete_dict.getlist('del_list')
            models.AuthInfo.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def put_assets(request):
        response = BaseResponse()
        try:
            response.error = []
            put_dict = QueryDict(request.body, encoding='utf-8')
            update_list = json.loads(put_dict.get('update_list'))
            error_count = 0
            for row_dict in update_list:
                nid = row_dict.pop('nid')
                num = row_dict.pop('num')
                # print(row_dict)

                # 更新主机名
                host_name = row_dict.get('host_name')
                if host_name:
                    if re.search('[》>$&()<!#*]', row_dict['host_name']):
                        response.error.append({'num': num, 'message': '非法字符！'})
                        response.status = False
                        error_count += 1
                    else:
                        obj = models.AuthInfo.objects.filter(id=nid)
                        change_host_name(host_ip=obj[0].host_ip, host_name=row_dict['host_name'])
                        try:
                            models.AuthInfo.objects.filter(id=nid).update(**row_dict)
                        except Exception as e:
                            response.error.append({'num': num, 'message': str(e)})
                            response.status = False
                            error_count += 1
                else:
                    try:
                        models.AuthInfo.objects.filter(id=nid).update(**row_dict)
                    except Exception as e:
                        response.error.append({'num': num, 'message': str(e)})
                        response.status = False
                        error_count += 1
            if error_count:
                response.message = '非法字符！共%s条,失败%s条' % (len(update_list), error_count,)
            else:
                response.message = '更新成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
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

    @staticmethod
    def post_assets(request):
        response = BaseResponse()

        ip = request.POST.get('ip')
        username = request.POST.get('username')
        user_rank = request.POST.get('user_rank')
        email = request.POST.get('email')

        record = models.AuthInfo.objects.filter(username=username, ip=ip, rank=user_rank).count()
        if record > 0:
            response.status = False
            response.message = '不能重复申请'
            return response
        try:
            models.AuthInfo.objects.create(username=username, ip=ip, rank=user_rank, email=email)
        except Exception as e:
            response.status = False
            response.message = str(e)
            return response
        response.status = True
        return response


