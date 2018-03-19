#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.db import models
from django import forms
from pytz import timezone
from django.utils import timezone
import datetime
from pytz import timezone

# utc_zone = timezone("utc")
# my_zone = timezone("Asia/Shanghai")
# my_time = datetime.datetime.utcnow().replace(tzinfo=utc_zone)
# out_time = my_time.astimezone(my_zone)


class AuthInfo(models.Model):
    """
    用户堡垒机权限表
    """
    auth_rank_choices = (
        (1, 'root'),
        (2, 'admin'),
        (3, 'rd')
    )
    auth_rank_status = (
        (1, '[申请中]'),
        (2, '[已通过]'),
        (3, '[已拒绝]')
    )
    username = models.CharField(max_length=32, null=True, blank=True)
    ip = models.CharField(max_length=32, null=True, blank=True)
    hostname = models.CharField(max_length=64, null=True, blank=True)
    rank = models.IntegerField(choices=auth_rank_choices, default=3)
    status = models.IntegerField(choices=auth_rank_status, default=1)
    email = models.CharField(max_length=64, null=True, blank=True)
    ctime = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "用户堡垒机权限表"

    def __str__(self):
        return self.username


class MachineType(models.Model):
    """
    虚拟机配置类型表
    """
    machine_type = models.CharField(max_length=32)
    machine_ip = models.CharField(max_length=32, null=True, blank=True)
    machine_host = models.CharField(max_length=32, null=True, blank=True)
    machine_name = models.CharField(max_length=32, null=True, blank=True)
    machine_xml_name = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        verbose_name_plural = "虚拟机配置类型表"

    def __str__(self):
        return self.machine_type


class HostMachines(models.Model):
    host_machines_ip = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "宿主机表"

    def __str__(self):
        return self.host_machines_ip


class PhysicalMachines(models.Model):
    """
    物理机
    """
    host_name = models.CharField(max_length=108)
    host_ip = models.CharField(max_length=32)
    item = models.CharField(max_length=32)
    bussiness = models.CharField(max_length=32, default='kvm-test')
    ctime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "物理机表"

    def __str__(self):
        return self.host_name


class VirtualMachines(models.Model):
    """
    虚拟机
    """
    mudroom_host = models.CharField(max_length=32,default='192.168.1.1')
    host_name = models.CharField(max_length=108)
    host_ip = models.CharField(max_length=32)
    bussiness = models.CharField(max_length=32, default='kvm-test')
    ctime = models.DateTimeField(auto_now_add=True)
    machine_type = models.ForeignKey('MachineType', to_field='id', default=1)
    cpu_num = models.IntegerField(default=2)
    memory_num = models.IntegerField(default=2)

    class Meta:
        verbose_name_plural = "虚拟机表"

    def __str__(self):
        return self.host_name


class Asset(models.Model):
    """
    资产信息总表
    """
    device_type_choices = (
        (1, '物理服务器'),
        (2, '虚拟机'),
        (3, '交换机'),
        (4, '防火墙'),
        (5, 'Docker'),
    )
    device_status_choices = (
        (1, '在线'),
        (2, '离线'),
    )
    device_item_choices = (
        (1, '已装机'),
        (2, '未装机'),
        (3, '故障机'),
    )

    host_ip = models.CharField(max_length=32, null=True, blank=True)
    host_name = models.CharField(max_length=128, null=True, blank=True)
    host_status = models.IntegerField(choices=device_status_choices, default=2)
    host_item = models.IntegerField(choices=device_item_choices, default=1)
    business_1 = models.ForeignKey('BusinessOne', verbose_name='业务线1', null=True, blank=True, default=1, on_delete=models.SET_DEFAULT)
    business_2 = models.ForeignKey('BusinessTwo', verbose_name='业务线2', null=True, blank=True, default=1, on_delete=models.SET_DEFAULT)
    business_3 = models.ForeignKey('BusinessThree', verbose_name='业务线3', null=True, blank=True, default=1, on_delete=models.SET_DEFAULT)
    host_type = models.IntegerField(choices=device_type_choices, default=2)
    host_machine = models.CharField(max_length=32, null=True, blank=True)
    host_cpu = models.CharField(max_length=32, null=True, blank=True)
    host_memory = models.CharField(max_length=32, null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "资产总表"

    def __str__(self):
        return "%s-%s-%s" % (self.host_ip, self.host_name, self.host_status)


class BusinessOne(models.Model):
    """
    一级业务线
    """
    name = models.CharField('一级业务线', max_length=64, unique=True)
    # contact = models.ForeignKey('UserGroup', verbose_name='业务联系人', related_name='c')
    # manager = models.ForeignKey('UserGroup', verbose_name='系统管理员', related_name='m')

    class Meta:
        verbose_name_plural = "一级业务线表"

    def __str__(self):
        return self.name


class BusinessTwo(models.Model):
    """
    二级业务线
    """
    name = models.CharField('二级业务线', max_length=64, unique=True)
    # business_url = models.CharField('业务线接口地址', max_length=64, null=True, blank=True)
    business_remark = models.CharField('备注', max_length=128, null=True, blank=True)

    class Meta:
        verbose_name_plural = "二级业务线表"

    def __str__(self):
        return self.name


class BusinessThree(models.Model):
    """
    三级业务线
    """
    name = models.CharField('三级业务线', max_length=64, unique=True)
    # superior_business = models.ForeignKey('BusinessTwo', verbose_name='二级业务线', related_name='b1')

    class Meta:
        verbose_name_plural = "三级业务线表"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """
    用户信息
    """
    name = models.CharField(u'姓名', max_length=32)
    group = models.ForeignKey('UserGroup', null=True, blank=True, default=2, on_delete=models.SET_DEFAULT)
    business_one = models.ManyToManyField('BusinessOne', null=True, blank=True)
    business_two = models.ManyToManyField('BusinessTwo', null=True, blank=True)
    business_three = models.ManyToManyField('BusinessThree', null=True, blank=True)

    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.name


class AdminInfo(forms.ModelForm):
    """
    用户登陆相关信息
    """
    user_info = models.OneToOneField("UserProfile")
    username = models.CharField(u'用户名', max_length=64)
    # password = models.CharField(u'密码', max_length=64)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    class Meta:
        verbose_name_plural = "管理员表"

    def __str__(self):
        return self.username


class UserGroup(models.Model):
    """
    用户组
    """
    name = models.CharField(max_length=32, unique=True)
    business_one = models.ManyToManyField('BusinessOne')
    business_two = models.ManyToManyField('BusinessTwo')
    business_three = models.ManyToManyField('BusinessThree')

    class Meta:
        verbose_name_plural = "用户组表"

    def __str__(self):
        return self.name


class ReleaseType(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        verbose_name_plural = "发布类型表"

    def __str__(self):
        return self.name


class ProjectTask(models.Model):
    """
    发布项目表
    """
    jdk_version_choice = (
        (1, 'jdk-8'),
        (2, 'jdk-7'),
        (3, 'jdk-6')
    )

    project_status_choice = (
        (1, '新提交'),
        (2, '发布成功'),
        (3, '发布失败'),
    )

    static_cover_type = (
        (1, '迭代'),
        (2, '覆盖')
    )

    business_1 = models.ForeignKey(BusinessOne, null=True, blank=True, default=1, on_delete=models.SET_DEFAULT)
    business_2 = models.ForeignKey(BusinessTwo, null=True, blank=True, default=2, on_delete=models.SET_DEFAULT)
    project_type = models.ForeignKey(ReleaseType, null=True, blank=True, default=1, on_delete=models.SET_NULL)
    jdk_version = models.IntegerField(choices=jdk_version_choice, null=True, blank=True)
    static_type = models.IntegerField(choices=static_cover_type, null=True, blank=True)
    release_last_id = models.CharField(max_length=32, null=True, blank=True, default='-')
    release_last_time = models.CharField(max_length=32, null=True, blank=True, default='-')
    release_user = models.CharField(max_length=32, null=True, blank=True)
    git_url = models.CharField(max_length=108, null=True, blank=True)
    pack_cmd = models.CharField(max_length=108, null=True, blank=True)
    git_branch = models.CharField(max_length=108, null=True, blank=True)
    status = models.IntegerField(choices=project_status_choice, null=True, blank=True, default=1)
    ctime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "项目表"

    def __str__(self):
        return self.business_2


class ReleaseTask(models.Model):
    """
    发布任务记录表
    """
    release_status_choices = (
        (1, '发布中'),
        (2, '发布成功'),
        (3, '发布失败'),
        (4, 'PM待审'),
        (5, 'DB待审'),
        (6, 'SA待审'),
        (7, '待发布'),
        (8, '已撤销'),
    )

    jdk_version_choice = (
        (1, 'JDK-8'),
        (2, 'JDK-7'),
        (3, 'JDK-6')
    )

    release_id = models.IntegerField(null=True, blank=True)
    release_name = models.ForeignKey(BusinessTwo, null=True, blank=True, default=1, on_delete=models.SET_NULL)
    release_env = models.ForeignKey(BusinessOne, null=True, blank=True, default=2, on_delete=models.SET_NULL)
    release_time = models.CharField(max_length=32, null=True, blank=True)
    release_status = models.IntegerField(choices=release_status_choices, null=True, blank=True, default=1)
    release_user = models.CharField(max_length=32, null=True, blank=True)
    release_git_url = models.CharField(max_length=64, null=True, blank=True)
    release_git_branch = models.CharField(max_length=32, null=True, blank=True)
    release_type = models.ForeignKey(ReleaseType, null=True, blank=True, on_delete=models.SET_NULL)
    release_jdk_version = models.IntegerField(choices=jdk_version_choice, null=True, blank=True)
    release_md5 = models.CharField(max_length=64, null=True, blank=True)
    apply_user = models.CharField(max_length=32, null=True, blank=True)
    apply_time = models.CharField(max_length=32, null=True, blank=True)
    check_user = models.CharField(max_length=32, null=True, blank=True)
    check_time = models.CharField(max_length=32, null=True, blank=True)
    release_reason = models.CharField(max_length=1080, null=True, blank=True)
    release_db = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        verbose_name_plural = "发布任务记录表"

    def __str__(self):
        return self.release_name


class ReleaseLog(models.Model):
    """
    发布任务日志
    """
    release_id = models.IntegerField(null=True, blank=True)
    # release_time = models.DateTimeField('时间', default=my_time)
    release_msg = models.CharField('日志', max_length=1000, null=True, blank=True)
    release_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "发布任务日志"

    def __str__(self):
        return self.release_id


class AuditLog(models.Model):
    """
    发布审核流程日志
    """
    audit_id = models.IntegerField(null=True, blank=True)
    audit_msg = models.CharField('日志', max_length=1000, null=True, blank=True)
    audit_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "发布审核流程日志"

    def __str__(self):
        return self.audit_id


class VpnAccount(models.Model):
    """
    vpn账号
    """
    active_status = (
        (1, '正常'),
        (2, '冻结'),
    )
    name = models.CharField(max_length=32, null=True, blank=True)
    password = models.CharField(max_length=108, null=True, blank=True)
    register_time = models.CharField(max_length=32, blank=True, null=True)
    active = models.IntegerField(choices=active_status, null=True, blank=True)

    class Meta:
        verbose_name_plural = "vpn 账号表"

    def __str__(self):
        return self.vpn_name


class BusinessUnit(models.Model):
    """
    业务线
    """
    name = models.CharField('业务线', max_length=64)
    contact = models.ForeignKey('UserGroup', verbose_name='业务联系人', related_name='c')
    manager = models.ForeignKey('UserGroup', verbose_name='系统管理员', related_name='m')

    class Meta:
        verbose_name_plural = "业务线表"

    def __str__(self):
        return self.name


class IDC(models.Model):
    """
    机房信息
    """
    name = models.CharField('机房', max_length=32)
    floor = models.IntegerField('楼层', default=1)

    class Meta:
        verbose_name_plural = "机房表"

    def __str__(self):
        return self.name


class Assets(models.Model):
    """
    资产信息表，所有资产公共信息（交换机，服务器，虚拟机等）
    """
    device_type_choices = (
        (1, '服务器'),
        (2, '交换机'),
        (3, '防火墙'),
    )
    device_status_choices = (
        (1, '上架'),
        (2, '在线'),
        (3, '离线'),
        (4, '下架'),
    )

    device_type_id = models.IntegerField(choices=device_type_choices, default=1)
    device_status_id = models.IntegerField(choices=device_status_choices, default=1)

    cabinet_num = models.CharField('机柜号', max_length=30, null=True, blank=True)
    cabinet_order = models.CharField('机柜中序号', max_length=30, null=True, blank=True)

    idc = models.ForeignKey('IDC', verbose_name='IDC机房', null=True, blank=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name='属于的业务线', null=True, blank=True)

    tag = models.ManyToManyField('Tag')

    latest_date = models.DateField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "资产表"

    def __str__(self):
        return "%s-%s-%s" % (self.idc.name, self.cabinet_num, self.cabinet_order)


class Tag(models.Model):
    """
    资产标签
    """
    name = models.CharField('标签', max_length=32, unique=True)

    class Meta:
        verbose_name_plural = "标签表"

    def __str__(self):
        return self.name


class Physical(models.Model):
    """
    服务器信息
    """
    # asset = models.OneToOneField('Asset')

    hostname = models.CharField('主机名', max_length=128, unique=True)
    manage_ip = models.CharField('管理IP', max_length=32, null=True, blank=True)
    idc = models.CharField('IDC', max_length=32, null=True, blank=True)
    cabinet = models.CharField('机柜', max_length=32, null=True, blank=True)
    putaway = models.CharField('上架时间', max_length=32, null=True, blank=True)
    model = models.CharField('型号', max_length=64, null=True, blank=True)
    sn = models.CharField('SN号', max_length=64, db_index=True)
    cpu = models.ForeignKey('Cpu', verbose_name='CPU型号', null=True, blank=True, on_delete=models.SET_NULL)
    raid = models.CharField('Raid', max_length=8, null=True, blank=True)
    service = models.CharField('保修期', max_length=32, null=True, blank=True)

    class Meta:
        verbose_name_plural = "服务器表"

    def __str__(self):
        return self.hostname


class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset')
    management_ip = models.CharField('管理IP', max_length=64, blank=True, null=True)
    vlan_ip = models.CharField('VlanIP', max_length=64, blank=True, null=True)
    intranet_ip = models.CharField('内网IP', max_length=128, blank=True, null=True)
    sn = models.CharField('SN号', max_length=64, unique=True)
    manufacture = models.CharField(verbose_name=u'制造商', max_length=128, null=True, blank=True)
    model = models.CharField('型号', max_length=128, null=True, blank=True)
    port_num = models.SmallIntegerField('端口个数', null=True, blank=True)
    device_detail = models.CharField('设置详细配置', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "网络设备"


class Cpu(models.Model):
    """
    CPU类型
    """
    name = models.CharField('类型',  max_length=64, null=True, blank=True)

    class Meta:
        verbose_name_plural = "CPU表"

    def __str__(self):
        return self.name


class NIC(models.Model):
    """
    网卡信息
    """
    name = models.CharField('网卡名称', max_length=128, null=True, blank=True)
    hwaddr = models.CharField('网卡mac地址', max_length=64, null=True, blank=True)
    ipaddrs = models.CharField('ip地址', max_length=256, null=True, blank=True)
    switch_ip = models.CharField('上联交换机IP', max_length=64, null=True, blank=True)
    switch_port = models.CharField('上联交换机端口', max_length=64, null=True, blank=True)
    server_obj = models.ForeignKey('DellServer', related_name='nic', null=True, blank=True)

    class Meta:
        verbose_name_plural = "网卡表"

    def __str__(self):
        return self.name


class NetWork(models.Model):
    """
    网络设备
    """
    brand = models.CharField('品牌', max_length=32, null=True, blank=True)
    model = models.CharField('设备型号', max_length=32, null=True, blank=True)
    ip = models.CharField('管理IP', max_length=32, null=True, blank=True)
    sn = models.CharField('sn', max_length=32, null=True, blank=True)
    idc = models.CharField('机房', max_length=32, null=True, blank=True)
    cabinet = models.CharField('机柜', max_length=32, null=True, blank=True)
    putaway = models.CharField('上架日期', max_length=32, null=True, blank=True)
    service = models.CharField('保修日期', max_length=32, null=True, blank=True)
    asset = models.IntegerField('关联资产', null=True, blank=True)

    class Meta:
        verbose_name_plural = "网卡表"

    def __str__(self):
        return self.name


class Memory(models.Model):
    """
    内存信息
    """
    slot = models.CharField('插槽位', max_length=32)
    manufacturer = models.CharField('制造商', max_length=32, null=True, blank=True)
    model = models.CharField('型号', max_length=64)
    capacity = models.FloatField('容量', null=True, blank=True)
    sn = models.CharField('内存SN号', max_length=64, null=True, blank=True)
    speed = models.CharField('速度', max_length=16, null=True, blank=True)
    # server_obj = models.ForeignKey('Servers',related_name='memory')

    class Meta:
        verbose_name_plural = "内存表"

    def __str__(self):
        return self.slot


class AssetRecord(models.Model):
    """
    资产变更记录,creator为空时，表示是资产汇报的数据。
    """
    asset_obj = models.ForeignKey('Asset', related_name='ar')
    content = models.TextField(null=True)
    creator = models.ForeignKey('UserProfile', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "资产记录表"

    def __str__(self):
        return "%s-%s-%s" % (self.asset_obj.idc.name, self.asset_obj.cabinet_num, self.asset_obj.cabinet_order)


class ErrorLog(models.Model):
    """
    错误日志,如：agent采集数据错误 或 运行错误
    """
    asset_obj = models.ForeignKey('Asset', null=True, blank=True)
    title = models.CharField(max_length=16)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "错误日志表"

    def __str__(self):
        return self.title


class DellServer(models.Model):
    """
    服务器信息
    """
    device_item_choices = (
        (1, '已装机'),
        (2, '未装机'),
        (3, '故障机'),
    )

    asset_id = models.IntegerField('资产', null=True, blank=True)

    hostname = models.CharField('主机名', max_length=128, null=True, blank=True)
    manage_ip = models.CharField('管理IP', max_length=32, null=True, blank=True)
    idc = models.CharField('IDC', max_length=32, null=True, blank=True)
    cabinet = models.CharField('机柜', max_length=32, null=True, blank=True)
    putaway = models.CharField('上架时间', max_length=32, null=True, blank=True)
    cpu_num = models.IntegerField('cpu核数', null=True, blank=True)
    core_num = models.IntegerField('cpu核数', null=True, blank=True)
    os = models.CharField('操作系统', max_length=32, null=True, blank=True)
    model = models.CharField('型号', max_length=64, null=True, blank=True)
    sn = models.CharField('SN号', max_length=64, db_index=True)
    cpu = models.ForeignKey('Cpu', verbose_name='CPU型号', null=True, blank=True, on_delete=models.SET_NULL)
    raid = models.CharField('Raid', max_length=8, null=True, blank=True)
    service = models.CharField('保修期', max_length=32, null=True, blank=True)
    physical_server_status = models.IntegerField(choices=device_item_choices, default=2)

    class Meta:
        verbose_name_plural = "服务器表"

    def __str__(self):
        return self.hostname


class HardDisk(models.Model):
    """
    硬盘信息
    """
    slot = models.CharField('插槽位', max_length=8, null=True, blank=True)
    model = models.CharField('磁盘型号', max_length=32, null=True, blank=True)
    capacity = models.FloatField('磁盘容量GB', null=True, blank=True)
    rpm = models.IntegerField('磁盘转速', null=True, blank=True)
    pd_type = models.CharField('磁盘类型', max_length=32, null=True, blank=True)
    server_obj = models.ForeignKey('DellServer', related_name='disk', null=True, blank=True)

    class Meta:
        verbose_name_plural = "硬盘表"

    def __str__(self):
        return self.slot


class DockerNode(models.Model):
    """
    Docker物理节点机器
    """
    ip = models.CharField(max_length=32, null=True, blank=True)
    create_time = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        verbose_name_plural = "docker物理节点表"

    def __str__(self):
        return self.ip


class DockerInfo(models.Model):
    """
    记录容器详细信息
    """
    name = models.CharField(max_length=108, null=True, blank=True)
    ip = models.CharField(max_length=32, null=True, blank=True)
    create_user = models.CharField(max_length=32, null=True, blank=True)
    docker_info = models.CharField(max_length=128, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    remove_time = models.CharField(max_length=32, null=True, blank=True)
    image = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        verbose_name_plural = "docker容器信息查询表"

    def __str__(self):
        return self.name


class Vlan(models.Model):
    """
    网段Vlan信息
    """
    vlan = models.CharField(max_length=32, unique=True)
    network = models.CharField(max_length=32, unique=True)
    netmask = models.CharField(max_length=32, null=True, blank=True)
    gateway = models.CharField(max_length=32, null=True, blank=True)
    usable = models.IntegerField(null=True, blank=True)
    disabled = models.IntegerField(null=True, blank=True)
    online = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Vlan表"

    def __str__(self):
        return self.vlan


class IpPool(models.Model):
    """
    IP池
    """
    ip_status_choices = (
        (1, '在线'),
        (2, '空闲'),
        (3, '禁用'),
    )
    ip = models.GenericIPAddressField(null=True, blank=True)
    network = models.GenericIPAddressField(null=True, blank=True)
    vlan = models.GenericIPAddressField(null=True, blank=True)
    gateway = models.GenericIPAddressField(null=True, blank=True)
    remark = models.CharField(max_length=108, null=True, blank=True)
    status = models.IntegerField(choices=ip_status_choices, default=2)

    class Meta:
        verbose_name_plural = "IP地址池"

    def __str__(self):
        return self.ip


class PhysicsInstall(models.Model):
    """
    物理机系统安装
    """
    install_status_choices = (
        (1, '待安装'),
        (2, '安装中'),
        (3, '已安装'),
        (4, '已撤销'),
    )
    sn = models.CharField(max_length=108, unique=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    hostname = models.CharField(max_length=108, null=True, blank=True)
    raid_level = models.IntegerField(null=True, blank=True)
    switch_ip = models.GenericIPAddressField(null=True, blank=True)
    switch_interface = models.IntegerField(null=True, blank=True)
    ilo_ip = models.GenericIPAddressField(null=True, blank=True)
    server_model = models.CharField(max_length=108, null=True, blank=True)
    os_version = models.CharField(max_length=108, null=True, blank=True)
    vlan = models.CharField(max_length=32, null=True, blank=True)
    netmask = models.IntegerField(null=True, blank=True)
    gateway = models.GenericIPAddressField(null=True, blank=True)
    status = models.IntegerField(choices=install_status_choices, default=1)

    class Meta:
        verbose_name_plural = "装机任务表"

    def __str__(self):
        return self.sn





