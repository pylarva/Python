# !/usr/bin/env python
# -*- coding:utf-8 -*-

# jenkins配置
host = '192.168.31.80'
jenkins_host = '192.168.31.10'

script_path = '/opt/autopublishing.py'

server_url = 'http://192.168.31.80:8080'

user_name = 'sa'

api_token = '9e235779d590f7c63d45201bb8c969be'

pkgUrl = 'http://build.xxd.com:8080'
# pkgUrl = 'http://192.168.31.10'

source_script_path = '/application/xxdCmdb/scr/autopublishing.py'
# source_script_path = '/Users/pylarva/github/Python/Projects/xxdCmdb/scr/autopublishing.py'

# 需要进行两次发布的项目
static_nginx_dict = {'front': '/static/front/', 'webapp': '/static/webapp/'}

# 配置文件存放目录
config_path = '/opt/config/'
# config_path = '/opt/config/'

# Nginx服务器
# 测试环境nginx机器
nginx_test_ip_list = ['192.168.33.110']

# 生产环境nginx机器
nginx_prod_ip_list = ['10.96.1.69', '10.96.1.70', '10.96.1.71']
# nginx_prod_ip_list = ['192.168.33.110']


# 静态资源包
static_pkg_name = {'mui': 'build', 'mobile': 'html', 'html': 'html', 'pc': 'build', 'apk': 'apk', 'm': 'dist',
                   'digital': 'digital', 'jk': 'jk', 'csm': 'csm'}

# 刷新cdn地址
cdn_url_1 = 'http://download-cdn.xinxindai.com/'
cdn_url_2 = 'https://download-cdn.xinxindai.com/'

# 配置文件修改 日志地址
run_log = '/home/admin/logs/run.log'
err_log = '/home/admin/logs/err.log'

# run_log = '/opt/logs/run.log'
# err_log = '/opt/logs/err.log'

# 容器挂载目录
container_mount_inside = '/opt/webapps'
container_mount_outside = '/opt/webapps'

# 容器自定义IP地址网关末位地址
container_gateway_ip = '253'

# 容器主机名
container_host_name = 'a0-docker-AA-BB-CC-DD.yh'

# 是否采用容器化的jenkins发布（1:是 0:否 即使用原有jenkins服务器打包 build.xxd.com）
jenkins_docker_switch = 0

# 灰度发布开关 0关 1开
gray_release = 1

# 灰度发布使用的consul地址
consul_ip = '10.96.1.196:8500'
