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
from utils.auditlog import audit_log


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
                'display': 1,
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
                    'content': "<i class='fa fa-exclamation-triangle' aria-hidden='true'></i><a href='#' style='text-decoration: none;' onclick='audit_pass({id})'> 审核通过 |</a>"
                               "<a href='/release-{id}.html' target='_blank'> 发布详细</a>",
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
        condition_dict['release_status'].append('5')

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

    @staticmethod
    def post_assets(request):
        response = BaseResponse()

        release_id = request.POST.get('audit_id', None)
        user = request.session['username']

        models.ReleaseTask.objects.filter(id=release_id).update(release_status=6)
        audit_log(release_id, '[ %s ] DB审核通过' % user)
        audit_log(release_id, '[ 系统 ] 等待SA审核..')

        response.status = True
        return response

