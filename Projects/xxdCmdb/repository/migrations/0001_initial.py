# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-31 06:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_ip', models.CharField(blank=True, max_length=32, null=True)),
                ('host_name', models.CharField(blank=True, max_length=128, null=True)),
                ('host_status', models.IntegerField(choices=[(1, '在线'), (2, '离线')], default=2)),
                ('host_item', models.IntegerField(choices=[(1, 'c1'), (2, 'c2')], default=1)),
                ('host_type', models.IntegerField(choices=[(1, '物理服务器'), (2, '虚拟机'), (3, '交换机'), (4, '防火墙')], default=2)),
                ('host_machine', models.CharField(blank=True, max_length=32, null=True)),
                ('host_cpu', models.CharField(blank=True, max_length=32, null=True)),
                ('host_memory', models.CharField(blank=True, max_length=32, null=True)),
                ('ctime', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': '资产总表',
            },
        ),
        migrations.CreateModel(
            name='AssetRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('asset_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ar', to='repository.Asset')),
            ],
            options={
                'verbose_name_plural': '资产记录表',
            },
        ),
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_type_id', models.IntegerField(choices=[(1, '服务器'), (2, '交换机'), (3, '防火墙')], default=1)),
                ('device_status_id', models.IntegerField(choices=[(1, '上架'), (2, '在线'), (3, '离线'), (4, '下架')], default=1)),
                ('cabinet_num', models.CharField(blank=True, max_length=30, null=True, verbose_name='机柜号')),
                ('cabinet_order', models.CharField(blank=True, max_length=30, null=True, verbose_name='机柜中序号')),
                ('latest_date', models.DateField(null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '资产表',
            },
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audit_id', models.IntegerField(blank=True, null=True)),
                ('audit_msg', models.CharField(blank=True, max_length=1000, null=True, verbose_name='日志')),
                ('audit_time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': '发布审核流程日志',
            },
        ),
        migrations.CreateModel(
            name='AuthInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=32, null=True)),
                ('ip', models.CharField(blank=True, max_length=32, null=True)),
                ('hostname', models.CharField(blank=True, max_length=64, null=True)),
                ('rank', models.IntegerField(choices=[(1, 'root'), (2, 'admin'), (3, 'rd')], default=3)),
                ('status', models.IntegerField(choices=[(1, '[申请中]'), (2, '[已通过]'), (3, '[已拒绝]')], default=1)),
                ('email', models.CharField(blank=True, max_length=64, null=True)),
                ('ctime', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': '用户堡垒机权限表',
            },
        ),
        migrations.CreateModel(
            name='BusinessOne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='一级业务线')),
            ],
            options={
                'verbose_name_plural': '一级业务线表',
            },
        ),
        migrations.CreateModel(
            name='BusinessThree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='三级业务线')),
            ],
            options={
                'verbose_name_plural': '三级业务线表',
            },
        ),
        migrations.CreateModel(
            name='BusinessTwo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='二级业务线')),
            ],
            options={
                'verbose_name_plural': '二级业务线表',
            },
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='业务线')),
            ],
            options={
                'verbose_name_plural': '业务线表',
            },
        ),
        migrations.CreateModel(
            name='Cpu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='类型')),
            ],
            options={
                'verbose_name_plural': 'CPU表',
            },
        ),
        migrations.CreateModel(
            name='DellServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_id', models.IntegerField(blank=True, null=True, verbose_name='资产')),
                ('hostname', models.CharField(blank=True, max_length=128, null=True, verbose_name='主机名')),
                ('manage_ip', models.CharField(blank=True, max_length=32, null=True, verbose_name='管理IP')),
                ('idc', models.CharField(blank=True, max_length=32, null=True, verbose_name='IDC')),
                ('cabinet', models.CharField(blank=True, max_length=32, null=True, verbose_name='机柜')),
                ('putaway', models.CharField(blank=True, max_length=32, null=True, verbose_name='上架时间')),
                ('cpu_num', models.IntegerField(blank=True, null=True, verbose_name='cpu核数')),
                ('core_num', models.IntegerField(blank=True, null=True, verbose_name='cpu核数')),
                ('os', models.CharField(blank=True, max_length=32, null=True, verbose_name='操作系统')),
                ('model', models.CharField(blank=True, max_length=64, null=True, verbose_name='型号')),
                ('sn', models.CharField(db_index=True, max_length=64, verbose_name='SN号')),
                ('raid', models.CharField(blank=True, max_length=8, null=True, verbose_name='Raid')),
                ('service', models.CharField(blank=True, max_length=32, null=True, verbose_name='保修期')),
                ('cpu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.Cpu', verbose_name='CPU型号')),
            ],
            options={
                'verbose_name_plural': '服务器表',
            },
        ),
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=16)),
                ('content', models.TextField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('asset_obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.Asset')),
            ],
            options={
                'verbose_name_plural': '错误日志表',
            },
        ),
        migrations.CreateModel(
            name='HardDisk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.CharField(blank=True, max_length=8, null=True, verbose_name='插槽位')),
                ('model', models.CharField(blank=True, max_length=32, null=True, verbose_name='磁盘型号')),
                ('capacity', models.FloatField(blank=True, null=True, verbose_name='磁盘容量GB')),
                ('rpm', models.IntegerField(blank=True, null=True, verbose_name='磁盘转速')),
                ('pd_type', models.CharField(blank=True, max_length=32, null=True, verbose_name='磁盘类型')),
                ('server_obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disk', to='repository.DellServer')),
            ],
            options={
                'verbose_name_plural': '硬盘表',
            },
        ),
        migrations.CreateModel(
            name='HostMachines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_machines_ip', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name_plural': '宿主机表',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='机房')),
                ('floor', models.IntegerField(default=1, verbose_name='楼层')),
            ],
            options={
                'verbose_name_plural': '机房表',
            },
        ),
        migrations.CreateModel(
            name='MachineType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine_type', models.CharField(max_length=32)),
                ('machine_ip', models.CharField(blank=True, max_length=32, null=True)),
                ('machine_host', models.CharField(blank=True, max_length=32, null=True)),
                ('machine_name', models.CharField(blank=True, max_length=32, null=True)),
                ('machine_xml_name', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'verbose_name_plural': '虚拟机配置类型表',
            },
        ),
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.CharField(max_length=32, verbose_name='插槽位')),
                ('manufacturer', models.CharField(blank=True, max_length=32, null=True, verbose_name='制造商')),
                ('model', models.CharField(max_length=64, verbose_name='型号')),
                ('capacity', models.FloatField(blank=True, null=True, verbose_name='容量')),
                ('sn', models.CharField(blank=True, max_length=64, null=True, verbose_name='内存SN号')),
                ('speed', models.CharField(blank=True, max_length=16, null=True, verbose_name='速度')),
            ],
            options={
                'verbose_name_plural': '内存表',
            },
        ),
        migrations.CreateModel(
            name='NetWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(blank=True, max_length=32, null=True, verbose_name='品牌')),
                ('model', models.CharField(blank=True, max_length=32, null=True, verbose_name='设备型号')),
                ('ip', models.CharField(blank=True, max_length=32, null=True, verbose_name='管理IP')),
                ('sn', models.CharField(blank=True, max_length=32, null=True, verbose_name='sn')),
                ('idc', models.CharField(blank=True, max_length=32, null=True, verbose_name='机房')),
                ('cabinet', models.CharField(blank=True, max_length=32, null=True, verbose_name='机柜')),
                ('putaway', models.CharField(blank=True, max_length=32, null=True, verbose_name='上架日期')),
                ('service', models.CharField(blank=True, max_length=32, null=True, verbose_name='保修日期')),
                ('asset', models.IntegerField(blank=True, null=True, verbose_name='关联资产')),
            ],
            options={
                'verbose_name_plural': '网卡表',
            },
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('management_ip', models.CharField(blank=True, max_length=64, null=True, verbose_name='管理IP')),
                ('vlan_ip', models.CharField(blank=True, max_length=64, null=True, verbose_name='VlanIP')),
                ('intranet_ip', models.CharField(blank=True, max_length=128, null=True, verbose_name='内网IP')),
                ('sn', models.CharField(max_length=64, unique=True, verbose_name='SN号')),
                ('manufacture', models.CharField(blank=True, max_length=128, null=True, verbose_name='制造商')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='型号')),
                ('port_num', models.SmallIntegerField(blank=True, null=True, verbose_name='端口个数')),
                ('device_detail', models.CharField(blank=True, max_length=255, null=True, verbose_name='设置详细配置')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repository.Asset')),
            ],
            options={
                'verbose_name_plural': '网络设备',
            },
        ),
        migrations.CreateModel(
            name='NIC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='网卡名称')),
                ('hwaddr', models.CharField(blank=True, max_length=64, null=True, verbose_name='网卡mac地址')),
                ('ipaddrs', models.CharField(blank=True, max_length=256, null=True, verbose_name='ip地址')),
                ('switch_ip', models.CharField(blank=True, max_length=64, null=True, verbose_name='上联交换机IP')),
                ('switch_port', models.CharField(blank=True, max_length=64, null=True, verbose_name='上联交换机端口')),
                ('server_obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nic', to='repository.DellServer')),
            ],
            options={
                'verbose_name_plural': '网卡表',
            },
        ),
        migrations.CreateModel(
            name='Physical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=128, unique=True, verbose_name='主机名')),
                ('manage_ip', models.CharField(blank=True, max_length=32, null=True, verbose_name='管理IP')),
                ('idc', models.CharField(blank=True, max_length=32, null=True, verbose_name='IDC')),
                ('cabinet', models.CharField(blank=True, max_length=32, null=True, verbose_name='机柜')),
                ('putaway', models.CharField(blank=True, max_length=32, null=True, verbose_name='上架时间')),
                ('model', models.CharField(blank=True, max_length=64, null=True, verbose_name='型号')),
                ('sn', models.CharField(db_index=True, max_length=64, verbose_name='SN号')),
                ('raid', models.CharField(blank=True, max_length=8, null=True, verbose_name='Raid')),
                ('service', models.CharField(blank=True, max_length=32, null=True, verbose_name='保修期')),
                ('cpu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.Cpu', verbose_name='CPU型号')),
            ],
            options={
                'verbose_name_plural': '服务器表',
            },
        ),
        migrations.CreateModel(
            name='PhysicalMachines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(max_length=108)),
                ('host_ip', models.CharField(max_length=32)),
                ('item', models.CharField(max_length=32)),
                ('bussiness', models.CharField(default='kvm-test', max_length=32)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '物理机表',
            },
        ),
        migrations.CreateModel(
            name='ProjectTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jdk_version', models.IntegerField(blank=True, choices=[(1, 'jdk-8'), (2, 'jdk-7'), (3, 'jdk-6')], null=True)),
                ('static_type', models.IntegerField(blank=True, choices=[(1, '迭代'), (2, '覆盖')], null=True)),
                ('release_last_id', models.CharField(blank=True, default='-', max_length=32, null=True)),
                ('release_last_time', models.CharField(blank=True, default='-', max_length=32, null=True)),
                ('release_user', models.CharField(blank=True, max_length=32, null=True)),
                ('git_url', models.CharField(blank=True, max_length=108, null=True)),
                ('pack_cmd', models.CharField(blank=True, max_length=108, null=True)),
                ('git_branch', models.CharField(blank=True, max_length=108, null=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, '新提交'), (2, '发布成功'), (3, '发布失败')], default=1, null=True)),
                ('ctime', models.DateTimeField(auto_now_add=True, null=True)),
                ('business_1', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='repository.BusinessOne')),
                ('business_2', models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='repository.BusinessTwo')),
            ],
            options={
                'verbose_name_plural': '项目表',
            },
        ),
        migrations.CreateModel(
            name='ReleaseLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('release_id', models.IntegerField(blank=True, null=True)),
                ('release_msg', models.CharField(blank=True, max_length=1000, null=True, verbose_name='日志')),
                ('release_time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': '发布任务日志',
            },
        ),
        migrations.CreateModel(
            name='ReleaseTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('release_id', models.IntegerField(blank=True, null=True)),
                ('release_time', models.CharField(blank=True, max_length=32, null=True)),
                ('release_status', models.IntegerField(blank=True, choices=[(1, '发布中'), (2, '发布成功'), (3, '发布失败'), (4, 'PM待审'), (5, 'DB待审'), (6, 'SA待审'), (7, '待发布'), (8, '已撤销')], default=1, null=True)),
                ('release_user', models.CharField(blank=True, max_length=32, null=True)),
                ('release_git_url', models.CharField(blank=True, max_length=64, null=True)),
                ('release_git_branch', models.CharField(blank=True, max_length=32, null=True)),
                ('release_jdk_version', models.IntegerField(blank=True, choices=[(1, 'JDK-8'), (2, 'JDK-7'), (3, 'JDK-6')], null=True)),
                ('release_md5', models.CharField(blank=True, max_length=64, null=True)),
                ('apply_user', models.CharField(blank=True, max_length=32, null=True)),
                ('apply_time', models.CharField(blank=True, max_length=32, null=True)),
                ('check_user', models.CharField(blank=True, max_length=32, null=True)),
                ('check_time', models.CharField(blank=True, max_length=32, null=True)),
                ('release_reason', models.CharField(blank=True, max_length=1080, null=True)),
                ('release_db', models.CharField(blank=True, max_length=64, null=True)),
                ('release_env', models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.BusinessOne')),
                ('release_name', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.BusinessTwo')),
            ],
            options={
                'verbose_name_plural': '发布任务记录表',
            },
        ),
        migrations.CreateModel(
            name='ReleaseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'verbose_name_plural': '发布类型表',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='标签')),
            ],
            options={
                'verbose_name_plural': '标签表',
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('business_one', models.ManyToManyField(to='repository.BusinessOne')),
                ('business_three', models.ManyToManyField(to='repository.BusinessThree')),
                ('business_two', models.ManyToManyField(to='repository.BusinessTwo')),
            ],
            options={
                'verbose_name_plural': '用户组表',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('business_one', models.ManyToManyField(blank=True, null=True, to='repository.BusinessOne')),
                ('business_three', models.ManyToManyField(blank=True, null=True, to='repository.BusinessThree')),
                ('business_two', models.ManyToManyField(blank=True, null=True, to='repository.BusinessTwo')),
                ('group', models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='repository.UserGroup')),
            ],
            options={
                'verbose_name_plural': '用户表',
            },
        ),
        migrations.CreateModel(
            name='VirtualMachines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mudroom_host', models.CharField(default='192.168.1.1', max_length=32)),
                ('host_name', models.CharField(max_length=108)),
                ('host_ip', models.CharField(max_length=32)),
                ('bussiness', models.CharField(default='kvm-test', max_length=32)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('cpu_num', models.IntegerField(default=2)),
                ('memory_num', models.IntegerField(default=2)),
                ('machine_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='repository.MachineType')),
            ],
            options={
                'verbose_name_plural': '虚拟机表',
            },
        ),
        migrations.AddField(
            model_name='releasetask',
            name='release_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.ReleaseType'),
        ),
        migrations.AddField(
            model_name='projecttask',
            name='project_type',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.ReleaseType'),
        ),
        migrations.AddField(
            model_name='businessunit',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='c', to='repository.UserGroup', verbose_name='业务联系人'),
        ),
        migrations.AddField(
            model_name='businessunit',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='m', to='repository.UserGroup', verbose_name='系统管理员'),
        ),
        migrations.AddField(
            model_name='assets',
            name='business_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.BusinessUnit', verbose_name='属于的业务线'),
        ),
        migrations.AddField(
            model_name='assets',
            name='idc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.IDC', verbose_name='IDC机房'),
        ),
        migrations.AddField(
            model_name='assets',
            name='tag',
            field=models.ManyToManyField(to='repository.Tag'),
        ),
        migrations.AddField(
            model_name='assetrecord',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.UserProfile'),
        ),
        migrations.AddField(
            model_name='asset',
            name='business_1',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='repository.BusinessOne', verbose_name='业务线1'),
        ),
        migrations.AddField(
            model_name='asset',
            name='business_2',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='repository.BusinessTwo', verbose_name='业务线2'),
        ),
        migrations.AddField(
            model_name='asset',
            name='business_3',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='repository.BusinessThree', verbose_name='业务线3'),
        ),
    ]
