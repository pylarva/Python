# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import logging

# logging.basicConfig(filename='example.log', level=logging.INFO,
#                     format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')
# logging.warning("user [kobe] attempted wrong password more than 3 times")
# logging.critical("Server is down...")

# 创建logger 谁去发日志
logger = logging.getLogger('TEST-LOG')  # 先获取logger对象
logger.setLevel(logging.DEBUG)  # 设置全局日志级别

# 创建Handler 发给屏幕
ch = logging.StreamHandler()  # 在屏幕上打印
ch.setLevel(logging.DEBUG)  # 设置在屏幕上打印日志的级别

# 创建Handler 文件文件
fh = logging.FileHandler("access.log")
fh.setLevel(logging.WARNING)
fh_err = logging.FileHandler("error.log")
fh_err.setLevel(logging.ERROR)

# 创建formatter输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter_for_file = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

# 分别设置格式
ch.setFormatter(formatter)
fh.setFormatter(formatter_for_file)
fh_err.setFormatter(formatter)

# 向logger注册
logger.addHandler(ch)
logger.addHandler(fh)
logger.addHandler(fh_err)

# 打印
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')