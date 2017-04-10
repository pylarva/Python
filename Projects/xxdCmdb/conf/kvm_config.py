# !/usr/bin/env python
# -*- coding:utf-8 -*-

# 虚拟机镜像存放目录
kvm_qcow_dir = '/opt/mv/'

# CentOS镜像版本
# key对应MachineType表
CentOS_6 = {

    '1': '/opt/mv/kvm-template-centos-6.4-20G-31-130.qcow2',
    '2': '/opt/mv/kvm-template-centos-6.4-100G-31-130.qcow2',
    '3': '/opt/mv/kvm-template-centos-6.4-300G-31-130.qcow2',

    '4': '/opt/mv/kvm-template-centos-7.2-20G-31-130.qcow2',
    '5': '/opt/mv/kvm-template-centos-7.2-100G-31-130.qcow2',
    '6': '/opt/mv/kvm-template-centos-7.2-300G-31-130.qcow2',
}

# 模版镜像统一IP
kvm_template_ip = '192.168.31.130'

# IP配置文件
kvm_template_ip_config = '/opt/ifcfig-eth0'

# ssh-key文件
ssh_key_file = '/Users/pylarva/.ssh/id_rsa'

# ssh超时时间
ssh_timeout = 3