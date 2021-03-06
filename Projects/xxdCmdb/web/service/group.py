#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from .base import BaseServiceList


class Group(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'name', 'text': '用户名', 'condition_type': 'input'},
        ]
        # 表格的配置
        table_config = [
            {
                'q': 'name',
                'title': "用户组名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {'name': 'name', 'id': '@name', 'origin': '@name', 'edit-enable': 'true',
                         'edit-type': 'input', }
            },
            {
                'q': 'business_one',
                'title': "环境",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@business_one'}},
                'attr': {'name': 'name', 'id': '@name', 'origin': '@name', 'edit-enable': 'true',
                         'edit-type': 'input', }
            },
            {
                'q': 'business_two',
                'title': "业务线2",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@business_two'}},
                'attr': {'name': 'name', 'id': '@name', 'origin': '@name', 'edit-enable': 'true',
                         'edit-type': 'input', }
            },
            {
                'q': 'business_three',
                'title': "业务线3",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@business_three'}},
                'attr': {'name': 'name', 'id': '@name', 'origin': '@name', 'edit-enable': 'true',
                         'edit-type': 'input', }
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<a href='#'>编辑</a>",
                    'kwargs': {'id': '@id', 'nid': '@id'}},
                'attr': {}
            },
        ]
        # 额外搜索条件
        extra_select = {}
        super(Group, self).__init__(condition_config, table_config, extra_select)

    def fetch_users(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.assets_condition(request)

            asset_count = models.UserGroup.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)

            asset_list = models.UserGroup.objects.filter(conditions).extra(select=self.extra_select).values(
                *self.values_list)[page_info.start:page_info.end]

            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(asset_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {}
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)

        return response

    @staticmethod
    def delete_users(request):
        response = BaseResponse()
        try:
            delete_dict = QueryDict(request.body, encoding='utf-8')
            id_list = delete_dict.getlist('id_list')
            models.UserGroup.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
            pass
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def put_users(request):
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
                    models.UserGroup.objects.filter(id=nid).update(**row_dict)
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
    def post_users(request):
        response = BaseResponse()

        new_group_name = request.POST.get('new_group_name', None)
        if new_group_name:
            try:
                models.UserGroup.objects.create(name=new_group_name)
                response.status = True
            except Exception as e:
                response.status = False
                response.message = ' %s 组已经存在!' % new_group_name
            return response

        del_group_id = request.POST.get('del_group_id', None)
        if del_group_id:
            try:
                models.UserGroup.objects.filter(id=del_group_id).delete()
                response.status = True
            except Exception as e:
                response.status = False
            return response

        nid = request.POST.get('nid')
        business_1 = request.POST.getlist('business_1_list')
        business_2 = request.POST.getlist('business_2_list')
        business_3 = request.POST.getlist('business_3_list')
        group_name = request.POST.getlist('group_name')[0]

        obj = models.UserGroup.objects.filter(id=nid).first()
        obj.name = group_name
        if business_1 == ['']:
            r = obj.business_one.all().values_list('id', flat=True)
            r = r[0:len(r)]
            for item in r:
                obj.business_one.remove(item)
        else:
            obj.business_one.set(business_1)

        if business_2 == ['']:
            r = obj.business_two.all().values_list('id', flat=True)
            r = r[0:len(r)]
            for item in r:
                obj.business_two.remove(item)
        else:
            obj.business_two.set(business_2)

        if business_3 == ['']:
            r = obj.business_three.all().values_list('id', flat=True)
            r = r[0:len(r)]
            for item in r:
                obj.business_three.remove(item)
        else:
            obj.business_three.set(business_3)

        obj.save()

        response.status = True
        return response
