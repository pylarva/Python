#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict
from .base import BaseServiceList


class Asset(BaseServiceList):
    def __init__(self):
        condition_config = [
            {'name': 'vlan', 'text': 'Vlan', 'condition_type': 'input'},
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
                'q': 'sn',
                'title': "SN",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@sn'}},
                'attr': {'name': 'sn', 'id': '@sn', 'original': '@sn',
                         'edit-enable': 'true',
                         'edit-type': 'input'}
            },
            {
                'q': 'ip',
                'title': "IP",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@ip'}},
                'attr': {'name': 'ip', 'id': '@ip', 'original': '@ip',
                         'edit-enable': 'true',
                         'edit-type': 'input'}
            },
            {
                'q': 'hostname',
                'title': "主机名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@hostname'}},
                'attr': {'name': 'hostname', 'id': '@hostname', 'original': '@hostname',
                         'edit-enable': 'true',
                         'edit-type': 'input'}
            },
            {
                'q': 'raid_level',
                'title': "RAID",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@raid_level'}},
                'attr': {'name': 'raid_level', 'id': '@raid_level', 'original': '@raid_level',
                         'edit-enable': 'true',
                         'edit-type': 'input'}
            },
            {
                'q': 'switch_ip',
                'title': "交换机",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@switch_ip'}},
                'attr': {'name': 'switch_ip', 'id': '@switch_ip', 'original': '@switch_ip',
                         'edit-enable': 'true',
                         'edit-type': 'input'}
            },
            {
                'q': 'switch_interface',
                'title': "交换机接口",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@switch_interface'}},
                'attr': {'name': 'switch_interface', 'id': '@switch_interface', 'original': '@switch_interface',
                         'edit-enable': 'true',
                         'edit-type': 'input'}
            },
            {
                'q': 'ilo_ip',
                'title': "ILO",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@ilo_ip'}},
                'attr': {'name': 'ilo_ip', 'id': '@ilo_ip', 'original': '@ilo_ip',
                         'edit-enable': 'true',
                         'edit-type': 'input'}
            },
            {
                'q': 'server_model',
                'title': "交换机",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@server_model'}},
                'attr': {'name': 'server_model', 'id': '@server_model', 'original': '@server_model',
                         'edit-enable': 'true',
                         'edit-type': 'input'}
            },
            {
                'q': 'os_version',
                'title': "OS",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@os_version'}},
                'attr': {'name': 'os_version', 'id': '@os_version', 'original': '@os_version',
                         'edit-enable': 'true',
                         'edit-type': 'input'}
            },
            {
                'q': 'vlan',
                'title': "VLAN",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@vlan'}},
                'attr': {'name': 'vlan', 'id': '@vlan', 'original': '@vlan',
                         'edit-enable': 'true',
                         'edit-type': 'input'}
            },
            {
                'q': 'gateway',
                'title': "网关",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@gateway'}},
                'attr': {'name': 'gateway', 'id': '@gateway', 'original': '@gateway',
                         'edit-enable': 'true',
                         'edit-type': 'input'}
            },
            {
                'q': 'status',
                'title': "状态",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@install_status_list'}},
                'attr': {'name': 'status', 'id': '@status', 'original': '@status',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'install_status_list'}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<i class='fa fa-check-circle' aria-hidden='true'></i><a href='#' onclick='do_release(this, {id})'> 开始安装</a> |"
                               "<a href='#' onclick='get_log({id}, false)'> 日志</a>",
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
    def install_status_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.PhysicsInstall.install_status_choices)
        return list(result)

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
            asset_count = models.PhysicsInstall.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            asset_list = models.PhysicsInstall.objects.filter(conditions).extra(select=self.extra_select).values(
                *self.values_list)[page_info.start:page_info.end]

            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(asset_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {
                'install_status_list': self.install_status_list,
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
            models.PhysicsInstall.objects.filter(id__in=id_list).delete()
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
                    models.PhysicsInstall.objects.filter(id=nid).update(**row_dict)
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
    def assets_info():
        response = BaseResponse()
        response.data = models.Cpu.objects.all()
        response.status = True
        return response

    @staticmethod
    def post_assets(request):
        response = BaseResponse()
        # 添加新的网段
        try:
            response.error = []
            vlan_name = request.POST.get('vlan_name')
            vlan_network = request.POST.get('vlan_network')
            vlan_netmask = request.POST.get('vlan_netmask')
            vlan_gateway = request.POST.get('vlan_gateway')
            # 检查是否重复添加

            # 添加新的网段成功前 将可用的IP地址添加到IP池 目前只做掩码是24位的自动添加
            ip_pool_list = []
            if int(vlan_netmask) != 24:
                response.status = False
                response.message = '暂时只支持掩码24位网段'
                return response
            else:
                new_ip = re.match('\d+\.\d+\.\d+\.', vlan_network).group()
                for ip in range(254):
                    new_ips = "%s%s" % (new_ip, ip)
                    ip_pool_list.append(models.IpPool(ip=new_ips, network=vlan_network, vlan=vlan_name,
                                                      gateway=vlan_gateway, status=2, remark=''))
                models.IpPool.objects.bulk_create(ip_pool_list)

            models.Vlan.objects.create(vlan=vlan_name, network=vlan_network, netmask=vlan_netmask,
                                       gateway=vlan_gateway)
            response.message = '添加成功'

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response






