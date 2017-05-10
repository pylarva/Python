#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from .base import BaseServiceList


class Asset(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'host_ip', 'text': 'IP', 'condition_type': 'input'},
            {'name': 'business_1', 'text': '环境', 'condition_type': 'select', 'global_name': 'business_1_list'},
            {'name': 'business_2', 'text': '二级业务线', 'condition_type': 'select', 'global_name': 'business_2_list'},
            {'name': 'business_3', 'text': '三级业务线', 'condition_type': 'select', 'global_name': 'business_3_list'},
        ]
        # 表格的配置
        table_config = [
            {
                'q': 'id',
                'title': "ID",
                'display': 0,
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {}
            },
            {
                'q': 'host_ip',
                'title': "IP",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@host_ip'}},
                'attr': {}
            },
            {
                'q': 'host_name',
                'title': "主机名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@host_name'}},
                'attr': {}
            },
            {
                'q': 'host_status',
                'title': "状态",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@device_status_list'}},
                'attr': {'name': 'host_status', 'id': '@host_status', 'origin': '@host_status',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'device_status_list'}
            },
            {
                'q': 'business_1_id',
                'title': "环境",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@business_1_list'}},
                'attr': {'name': 'business_1_id', 'id': '@business_1_id', 'origin': '@business_1_id', 'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'business_1_list'}
            },
            {
                'q': 'business_2_id',
                'title': "二级业务线",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@business_2_list'}},
                'attr': {'name': 'business_2_id', 'id': '@business_2_id', 'origin': '@business_2_id',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'business_2_list'}
            },
            {
                'q': 'business_3_id',
                'title': "三级业务线",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@business_3_list'}},
                'attr': {'name': 'business_3_id', 'id': '@business_3_id', 'origin': '@business_3_id',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'business_3_list'}
            },
            {
                'q': None,
                'title': "权限",
                'display': 1,
                'text': {
                    'content': "<select><option value='3'>rd</option><option value='2'>admin</option><option value='1'>root</option></select>",
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<a id=host_{nid} href='#' onclick=authorize(this,'{host_ip}','{nid}')>权限申请</a>",
                    'kwargs': {'nid': '@id', 'host_ip': '@host_ip'},
                    'attr': {}
                }
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
    def rank_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.auth_rank_choices)
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

    # @property
    def business_1_list(self, request):
        # 基于用户session用户名来查用户权限
        username = request.GET.get('username')

        # 先将用户组中的权限添加进condition
        obj = models.UserProfile.objects.filter(name=username).first()
        business_one_obj = obj.group.business_one.all()
        q = Q()
        q.connector = 'OR'
        for item in business_one_obj:
            print(item)
            q.children.append(('name', item))

        # 再将自定义的业务权限添加进condition
        business_one_modification = obj.business_one.all()
        for item in business_one_modification:
            print(item)
            q.children.append(('name', item))
        # q = self.get_authority(request)

        values = models.BusinessOne.objects.filter(q).only('id', 'name')
        result = map(lambda x: {'id': x.id, 'name': "%s" % x.name}, values)
        return list(result)

    # @property
    def business_3_list(self, request):
        username = request.GET.get('username')

        obj = models.UserProfile.objects.filter(name=username).first()
        business_three_obj = obj.group.business_three.all()
        q = Q()
        q.connector = 'OR'
        for item in business_three_obj:
            print(item)
            q.children.append(('name', item))

        business_three_modification = obj.business_three.all()
        for item in business_three_modification:
            print(item)
            q.children.append(('name', item))

        values = models.BusinessThree.objects.filter(q).only('id', 'name')
        result = map(lambda x: {'id': x.id, 'name': "%s" % x.name}, values)
        return list(result)

    # @property
    def business_2_list(self, request):
        username = request.GET.get('username')

        obj = models.UserProfile.objects.filter(name=username).first()
        business_two_obj = obj.group.business_two.all()
        q = Q()
        q.connector = 'OR'
        for item in business_two_obj:
            print(item)
            q.children.append(('name', item))

        business_two_modification = obj.business_two.all()
        for item in business_two_modification:
            print(item)
            q.children.append(('name', item))

        values = models.BusinessTwo.objects.filter(q).only('id', 'name')
        result = map(lambda x: {'id': x.id, 'name': "%s" % x.name}, values)
        return list(result)

    @property
    def business_unit_list(self):
        values = models.BusinessUnit.objects.values('id', 'name')
        return list(values)

    @staticmethod
    def get_authority(request):
        # 基于用户session用户名来查用户权限
        username = request.GET.get('username')

        # 1、业务1权限
        business_one_condition = Q()

        #    先将用户组中的权限添加进condition
        obj = models.UserProfile.objects.filter(name=username).first()
        business_one_obj = obj.group.business_one.all()
        business_one_condition.connector = 'OR'
        for item in business_one_obj:
            print(item)
            item = str(item)
            business_one_condition.children.append(('name', item))

        #    再将自定义的业务权限添加进condition
        business_one_modification = obj.business_one.all()
        for item in business_one_modification:
            print(item)
            item = str(item)
            business_one_condition.children.append(('name', item))

        # 2、业务2权限
        con_q = Q()
        con_q.add(business_one_condition, 'AND')

        print(business_one_condition)
        print(con_q)

        return business_one_condition, con_q

    @staticmethod
    def assets_condition(request):
        # 创建权限字典
        # condition_dict = {"business_1":["2","3"],"business_2":["3"],"business_3":["3"]}
        condition_dict = {"business_1": [], "business_2": [], "business_3": [], "host_ip__contains": []}

        # 开始根据用户名查权限
        username = request.GET.get('username')
        obj = models.UserProfile.objects.filter(name=username).first()

        # 用户组权限
        business_one_obj = obj.group.business_one.values('id')
        for item in business_one_obj:
            condition_dict['business_1'].append(str(item['id']))
        business_two_obj = obj.group.business_two.values('id')
        for item in business_two_obj:
            condition_dict['business_2'].append(str(item['id']))
        business_three_obj = obj.group.business_three.values('id')
        for item in business_three_obj:
            condition_dict['business_3'].append(str(item['id']))

        # 自定义权限
        business_one_m = obj.business_one.values('id')
        for item in business_one_m:
            condition_dict['business_1'].append(str(item['id']))
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
            asset_count = models.Asset.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            asset_list = models.Asset.objects.filter(conditions).extra(select=self.extra_select).values(
                *self.values_list)[page_info.start:page_info.end]

            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(asset_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            business_1_lists = self.business_1_list(request)
            business_2_lists = self.business_2_list(request)
            business_3_lists = self.business_3_list(request)
            ret['global_dict'] = {
                'device_status_list': self.device_status_list,
                'device_type_list': self.device_type_list,
                'idc_list': self.idc_list,
                'business_unit_list': self.business_unit_list,
                'business_1_list': business_1_lists,
                'business_2_list': business_2_lists,
                'business_3_list': business_3_lists
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
        response = BaseResponse()
        try:
            response.error = []
            put_dict = QueryDict(request.body, encoding='utf-8')
            update_list = json.loads(put_dict.get('update_list'))
            error_count = 0
            for row_dict in update_list:
                nid = row_dict.pop('nid')
                num = row_dict.pop('num')
                try:
                    models.Asset.objects.filter(id=nid).update(**row_dict)
                except Exception as e:
                    response.error.append({'num': num, 'message': str(e)})
                    response.status = False
                    error_count += 1
            if error_count:
                response.message = '共%s条,失败%s条' % (len(update_list), error_count,)
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