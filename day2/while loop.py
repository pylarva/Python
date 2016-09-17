#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

count = 0
while True:
    count += 1
    if count > 50 and count < 60:
        continue
    print("你是风儿我是沙，缠缠绵绵到天涯...",count)
    if count == 100:
        print("紫薇！紫薇！我是尔康啊紫薇...")
        break