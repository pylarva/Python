#!/usr/bin/env python
# coding: utf-8

# 666
import os
import json
import requests
import subprocess
import urllib.request

s = 'export PATH=/usr/local/node7/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin && npm install && npm run build'

s1 = s.split(' ')[1].split('=')[1].split(':')[0]
print(s1)