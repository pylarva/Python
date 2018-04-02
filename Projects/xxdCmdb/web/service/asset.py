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



class Asset(BaseServiceList):
    def __init__(self):
        condition_config = [
            {'name': 'host_ip', 'text': 'IP', 'condition_type': 'input'},
            {'name': 'business_1', 'text': '环境', 'condition_type': 'select', 'global_name': 'business_1_list'},
            {'name': 'host_name', 'text': '主机名', 'condition_type': 'input'},
            {'name': 'business_2', 'text': '二级业务线', 'condition_type': 'select', 'global_name': 'business_2_list'},
            {'name': 'business_3', 'text': '三级业务线', 'condition_type': 'select', 'global_name': 'business_3_list'},
            {'name': 'host_type', 'text': '资产类型', 'condition_type': 'select', 'global_name': 'device_type_list'},
            {'name': 'host_status', 'text': '在线状态', 'condition_type': 'select',
             'global_name': 'device_status_list'},
            {'name': 'host_item', 'text': '资产状态', 'condition_type': 'select',
             'global_name': 'physical_server_status'},
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
                'attr': {'name': 'host_name', 'id': '@host_name', 'original': '@host_name',
                         'edit-enable': 'true',
                         'edit-type': 'input'}
            },
            {
                'q': 'host_status',
                'title': "状态",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@device_status_list'}},
                'attr': {'name': 'host_status', 'id': '@host_status', 'original': '@host_status',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'device_status_list'}
            },
            {
                'q': 'business_1_id',
                'title': "环境",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@business_1_list'}},
                'attr': {'name': 'business_1_id', 'id': '@business_1_id', 'original': '@business_1_id', 'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'business_1_list'}
            },
            {
                'q': 'business_2_id',
                'title': "二级业务线",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@business_2_list'}},
                'attr': {'name': 'business_2_id', 'id': '@business_2_id', 'original': '@business_2_id',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'business_2_list'}
            },
            {
                'q': 'business_3_id',
                'title': "三级业务线",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@business_3_list'}},
                'attr': {'name': 'business_3_id', 'id': '@business_3_id', 'original': '@business_3_id',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'business_3_list'}
            },
            {
                'q': 'host_machine',
                'title': "宿主机",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@host_machine'}},
                'attr': {'name': 'host_machine', 'id': '@host_machine', 'original': '@host_machine',
                         'edit-enable': 'true',
                         'edit-type': 'input',
                         }
            },
            {
                'q': 'host_cpu',
                'title': "CPU",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@host_cpu'}},
                'attr': {}
            },
            {
                'q': 'host_memory',
                'title': "内存",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@host_memory'}},
                'attr': {}
            },
            {
                'q': 'host_type',
                'title': "设备类型",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@device_type_list'}},
                'attr': {'name': 'host_type', 'id': '@host_type', 'original': '@host_type',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'device_type_list'}
            },
            {
                'q': 'host_item',
                'title': "资产状态",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@physical_server_status'}},
                'attr': {'name': 'host_item', 'id': '@host_item', 'original': '@host_item',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'physical_server_status'}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<a href='/asset-{nid}.html' target='_blank'>查看详细</a>",
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
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.device_status_choices)
        return list(result)

    @property
    def device_type_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.device_type_choices)
        return list(result)

    @property
    def physical_server_status(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.device_item_choices)
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
            ret['global_dict'] = {
                'device_status_list': self.device_status_list,
                'device_type_list': self.device_type_list,
                'physical_server_status': self.physical_server_status,
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

    @staticmethod
    def assets_info():
        response = BaseResponse()
        response.data = models.Cpu.objects.all()
        response.status = True
        return response

    @staticmethod
    def post_assets(request):
        """
        添加资产信息
        :param request:
        :return:
        """

        response = BaseResponse()

        # 添加防火墙
        isfirewall = request.POST.get('isfirewall', None)

        if isfirewall:
            nic_brand = request.POST.get('fire_brand')
            nic_model = request.POST.get('fire_model')
            nic_ip = request.POST.get('fire_ip')
            nic_sn = request.POST.get('fire_sn')
            nic_idc = request.POST.get('fire_idc')
            nic_cabinet = request.POST.get('fire_cabinet')
            nic_putaway = request.POST.get('fire_putaway')
            nic_service = request.POST.get('fire_service')

            num = models.NetWork.objects.filter(sn=nic_sn).count()
            if num != 0:
                response.status = False
                response.message = '相同的sn资产已经存在！--%s' % nic_sn
                return response

            try:
                asset_obj = models.Asset(host_ip=nic_ip, host_name=nic_model, host_status=1, host_type=4, host_cpu=2,
                                         host_memory=2)
                asset_obj.save()

                models.NetWork.objects.create(model=nic_model, ip=nic_ip, idc=nic_idc, cabinet=nic_cabinet, sn=nic_sn,
                                              putaway=nic_putaway, service=nic_service, asset=asset_obj.id, brand=nic_brand)

            except Exception as e:
                response.status = False
                response.message = '添加资产错误'
                return response

            response.status = True
            return response

        # 添加网卡设备
        nic_model = request.POST.get('nic_model', None)
        if nic_model:
            nic_brand = request.POST.get('nic_brand')
            nic_ip = request.POST.get('nic_ip')
            nic_sn = request.POST.get('nic_sn')
            nic_idc = request.POST.get('nic_idc')
            nic_cabinet = request.POST.get('nic_cabinet')
            nic_putaway = request.POST.get('nic_putaway')
            nic_service = request.POST.get('nic_service')

            num = models.NetWork.objects.filter(sn=nic_sn).count()
            if num != 0:
                response.status = False
                response.message = '相同的sn资产已经存在！--%s' % nic_sn
                return response

            try:
                asset_obj = models.Asset(host_ip=nic_ip, host_name=nic_model, host_status=1, host_type=3, host_cpu=2,
                                         host_memory=2)
                asset_obj.save()

                models.NetWork.objects.create(model=nic_model, ip=nic_ip, idc=nic_idc, cabinet=nic_cabinet, sn=nic_sn,
                                              putaway=nic_putaway, service=nic_service, asset=asset_obj.id, brand=nic_brand)

            except Exception as e:
                response.status = False
                response.message = '添加资产错误'
                return response

            response.status = True
            return response

        host = request.POST.get('host')
        ip = request.POST.get('ip')
        memory = request.POST.get('memory')
        idc = request.POST.get('idc')
        cabinet = request.POST.get('cabinet')
        putaway = request.POST.get('putaway')
        machine = request.POST.get('machine')
        sn = request.POST.get('sn')
        cpu = request.POST.get('cpu')
        cpu_num = request.POST.get('cpu_num')
        core_num = request.POST.get('core_num')
        raid = request.POST.get('raid')
        service = request.POST.get('service')
        disk_list = request.POST.getlist('disk_list')
        nic_list = request.POST.getlist('nic_list')
        os = request.POST.get('os')
        physical_server_status = request.POST.get('physical_server_status')
        asset_serial_number = request.POST.get('asset_serial_number')
        is_hosts = request.POST.get('is_hosts')
        if is_hosts == 'true':
            is_hosts = 1
        else:
            is_hosts = 0

        for item in nic_list[2:]:
            item_list = item.split(',')
            ippaddrs = item_list[3]

        # 检查重复IP
        num = models.Asset.objects.filter(host_ip=ippaddrs).count()
        if num != 0:
            response.status = False
            response.message = '资产IP地址已经存在！'
            return response

        # 首先创建 Assets资产表 ➡️ 创建Server表关联Asset ➡️ 创建Disk表关联Server表 ➡️ 创建Memory表关联Server表
        asset_obj = models.Asset(host_ip=ippaddrs, host_name=host, host_status=1, host_type=1, host_cpu=int(cpu_num)*int(core_num), host_memory=memory,
                                 host_item=physical_server_status)
        asset_obj.save()

        server_obj = models.DellServer(asset_id=asset_obj.id, hostname=host, manage_ip=ip, idc=idc, cabinet=cabinet,
                                       putaway=putaway, model=machine, sn=sn, cpu_id=cpu, raid=raid, service=service,
                                       cpu_num=cpu_num, core_num=core_num, os=os,
                                       asset_serial_number=asset_serial_number, is_hosts=is_hosts)
        server_obj.save()

        # ['', '', ',1,500G,SAS,7200,SEAGATE ST300MM0006 LS08S0K2B5NV']
        for item in disk_list[2:]:
            item_list = item.split(',')
            slot = item_list[1]
            capacity = item_list[2]
            model = item_list[3]
            rpm = item_list[4]
            pd_type = item_list[5]
            disk_obj = models.HardDisk(slot=slot, capacity=capacity, model=model, rpm=rpm, pd_type=pd_type, server_obj_id=server_obj.id)
            disk_obj.save()

        # ['', '', ',eth0,00:1c:42:a5:57:7a,192.168.1.1,192.168.1.254,8']
        for item in nic_list[2:]:
            item_list = item.split(',')
            name = item_list[1]
            hwaddr = item_list[2]
            ippaddrs = item_list[3]
            switch_ip = item_list[4]
            switch_port = item_list[5]
            nic_obj = models.NIC(name=name, hwaddr=hwaddr, ipaddrs=ippaddrs, switch_ip=switch_ip,
                                 switch_port=switch_port, server_obj_id=server_obj.id)
            nic_obj.save()

        response.status = True
        return response


