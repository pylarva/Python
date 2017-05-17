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


class Project(BaseServiceList):
    def __init__(self):
        condition_config = [
            {'name': 'business_1', 'text': '环境', 'condition_type': 'input', 'condition_type': 'select', 'global_name': 'business_1_list'},
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
                'q': 'release_user',
                'title': "发起人",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@release_user'}},
                'attr': {}
            },
            {
                'q': 'business_1',
                'title': "环境",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@business_1_list'}},
                'attr': {'name': 'business_1', 'id': '@business_1', 'original': '@business_1',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'business_1_list'}
            },
            {
                'q': 'business_2',
                'title': "项目名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@business_2_list'}},
                'attr': {}
            },
            {
                'q': 'ctime',
                'title': "最新发布时间",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@ctime'}},
                'attr': {}
            },
            {
                'q': 'status',
                'title': "发布状态",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@device_status_list'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<i class='fa fa-edge' aria-hidden='true'></i><a href='/release-{nid}'>发布</a> | "
                               "<i class='fa fa-television' aria-hidden='true'></i><a href='#' onclick='del_group({{ obj.id }})'>详细</a>",
                    # 'content': "<a href='/asset-1-{nid}.html'>查看详细</a> | <a href='/edit-asset-{device_type_id}-{nid}.html'>编辑</a>",
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id'}},
                'attr': {}
            },
        ]
        # 额外搜索条件
        extra_select = {
            'server_title': 'select hostname from repository_server where repository_server.ProjectTask_id=repository_ProjectTask.id and repository_ProjectTask.device_type_id=1',
            'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.ProjectTask_id=repository_ProjectTask.id and repository_ProjectTask.device_type_id=2',
        }
        super(Project, self).__init__(condition_config, table_config, extra_select)

    @property
    def device_status_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.ProjectTask.project_status_choice)
        return list(result)

    @property
    def device_type_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.device_type_choices)
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

        print(con_q)

        return con_q

    def fetch_assets(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.assets_condition(request)
            asset_count = models.ProjectTask.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            asset_list = models.ProjectTask.objects.filter(conditions).extra(select=self.extra_select).values(
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
            models.ProjectTask.objects.filter(id__in=id_list).delete()
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
                        obj = models.Asset.objects.filter(id=nid)
                        change_host_name(host_ip=obj[0].host_ip, host_name=row_dict['host_name'])
                        try:
                            models.Asset.objects.filter(id=nid).update(**row_dict)
                            # 更新权限管理表中的主机名
                            models.AuthInfo.objects.filter(ip=obj[0].host_ip).update(hostname=host_name)
                        except Exception as e:
                            response.error.append({'num': num, 'message': str(e)})
                            response.status = False
                            error_count += 1
                else:
                    try:
                        models.Asset.objects.filter(id=nid).update(**row_dict)
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
                response.data = models.Server.objects.filter(asset_id=asset_id).select_related('ProjectTask').first()
            else:
                response.data = models.NetworkDevice.objects.filter(asset_id=asset_id).select_related('ProjectTask').first()

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

