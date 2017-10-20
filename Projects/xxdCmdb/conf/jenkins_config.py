# !/usr/bin/env python
# -*- coding:utf-8 -*-

# jenkins配置
host = '192.168.31.80'

script_path = '/opt/autopublishing.py'

server_url = 'http://192.168.31.80:8080'

user_name = 'sa'

api_token = '9e235779d590f7c63d45201bb8c969be'

pkgUrl = 'http://build.xxd.com'

# source_script_path = '/application/xxdCmdb/scr/autopublishing.py'
source_script_path = '/Users/pylarva/github/Python/Projects/xxdCmdb/scr/autopublishing.py'

# 需要进行两次发布的项目
static_nginx_dict = {'front': '/static/front/', 'webapp': '/static/webapp/'}

# 配置文件存放目录
config_path = '/opt/config/'
# config_path = '/opt/config/'

# Nginx服务器
# 测试环境nginx机器
nginx_test_ip_list = ['192.168.31.110', '192.168.33.110']

# 生产环境nginx机器
# nginx_prod_ip_list = ['10.96.1.69', '10.96.1.70', '10.96.1.71']
nginx_prod_ip_list = ['192.168.31.110', '192.168.33.110']


# 静态资源包
static_pkg_name = {'mui': 'build', 'mobile': 'html', 'html': 'html', 'pc': 'build', 'apk': 'apk', 'm': 'dist',
                   'digital': 'digital', 'jk': 'jk'}

# 刷新cdn地址
cdn_url_1 = 'http://download-cdn.xinxindai.com/'
cdn_url_2 = 'https://download-cdn.xinxindai.com/'

# 配置文件修改 日志地址
run_log = '/home/admin/logs/run.log'
err_log = '/home/admin/logs/err.log'

# run_log = '/opt/logs/run.log'
# err_log = '/opt/logs/err.log'
