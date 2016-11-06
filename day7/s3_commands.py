# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 1、和shell命令相关的模块
import subprocess

# 返回命令执行结果
# result = subprocess.call('ls -l', shell=True)
# result = subprocess.call(['ls', '-l'], shell=False)
# print(result)

# subprocess.check_call(["ls", "-l"])
# subprocess.check_call("exit 1", shell=True)

# 好像没Python废弃了
subprocess.check_output(["echo", "Hello World!"], shell=False)
subprocess.check_output("exit 1", shell=True)

# 2、执行复杂的系统相关命令

# 1）切换目录再执行命令
obj = subprocess.Popen("mkdir t3", shell=True, cwd='/home/dev',)

# 2）有多行且复杂的命令使用三个接口
# obj = subprocess.Popen(["python"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
# obj.stdin.write("print(1)\n")  # 传命令接口
# obj.stdin.write("print(2)")
# obj.stdin.close()
#
# cmd_out = obj.stdout.read()  # 读接口
# obj.stdout.close()
# cmd_error = obj.stderr.read()  # 读错误接口
# obj.stderr.close()
#
# print(cmd_out)
# print(cmd_error)

# 3）一次读输出
# obj = subprocess.Popen(["python"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
# obj.stdin.write("print(1)\n")
# obj.stdin.write("print(2)")
#
# out_error_list = obj.communicate()
# print(out_error_list)

# 4）简单写法
# obj = subprocess.Popen(["python"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
# out_error_list = obj.communicate('print("hello")')
# print(out_error_list)