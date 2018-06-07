# !/usr/bin/env python
# -*- coding:utf-8 -*-

# 虚拟机镜像存放目录
kvm_qcow_dir = '/opt/mv/'

# 模版镜像存放目录
kvm_template_dir = '/opt/mvs/'

# 虚拟机xml目录
kvm_xml_dir = '/opt/xml/'

# idc地址
kvm_addr = 'a2'

kvm_str = 'jd'

# 自定义网关地址
kvm_last_gateway = '254'

# 自动获取IP地址范围
kvm_range_ip = [51, 249]

# 模版镜像统一IP
kvm_template_ip = '192.168.31.130'

# IP配置文件
kvm_template_ip_config = '/opt/ifcfig-eth0'

# 初始主机名
kvm_template_hostname = 'kvm-vhost'

# xml文件目录
kvm_template_xml_dir = '/application/xxdCmdb/conf/xml/'

# xml配置文件
kvm_template_xml = '/application/xxdCmdb/conf/xml/template.xml'

# ssh-key文件
ssh_key_file = '/root/.ssh/id_rsa'

# ssh超时时间
ssh_timeout = 3

# 静态资源发布目录