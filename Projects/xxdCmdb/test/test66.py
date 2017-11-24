#!/usr/bin/env python
# coding: utf-8
import os

print(os.popen("ssh root@192.168.38.56 docker exec test01 ifconfig | awk 'NR==2 {print $2}'").read().strip())




