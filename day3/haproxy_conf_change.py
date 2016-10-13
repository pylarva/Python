#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing
import sys

# 打印登陆选项菜单
def menu_show():
    print(
        '''
*****************************************
**      Haproxy配置文件修改系统         **
*****************************************
1.获取HAproxy记录
2.增加HAproxy记录
3.删除HAproxy记录
4.退出系统
-----------------------------------------
        '''
    )

# 用户输入编号判断
def user_select():
    """
    用户输入的如果是1-4数字则return对应数字
    """
    while True:
        user_select = input("请输出编号： ")
        if user_select.isdigit():
            user_select =int(user_select)
            if user_select > 0 and user_select < 5:
                return user_select
            else:
                print("编号不存在...")
        else:
            print("输入错误...")

# 显示haproxy server信息
def haproxy_show():
    backend = input("请输入backend: ")

# 增加haproxy server函数
def haproxy_add():
# 删除haprxoy server函数
def haproxy_dell():

# 开始主程序
def main():
    menu_show()
    ret = user_select()
    if ret == 1:
        haproxy_show()
    if ret == 2:
        haproxy_add()
    if ret == 3:
        haproxy_dell()
    if ret == 4:
        print("退出系统成功！")
        sys.exit()


main()