#!/usr/bin/env python
# coding: utf-8

# 666
import os
import json
import requests
import subprocess
import urllib.request

json_data = []
config_path = '/opt/configure_files'
print(os.path.basename(config_path))

# {title:'编码', field:'code', candidate:false}


# def load_path(config_path, json_data):
#     pathList = os.listdir(config_path)
#     for i, item in enumerate(pathList):
#         config_dict = {}
#
#         config_dict['title'] = item
#         config_dict['open'] = 'false'
#         config_dict['field'] = os.path.join(config_path, item)
#         config_dict['candidate'] = 'true'
#
#         if os.path.isdir(os.path.join(config_path, item)):
#             config_dict['children'] = []
#             config_dict['children'] = load_path(os.path.join(config_path, item), config_dict['children'])
#
#         json_data.append(config_dict)
#     return json_data
#
# json_data = load_path(config_path, json_data)
# print(json_data)
