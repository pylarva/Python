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
