#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing
import sys,os,time

id_db = {
    '亚洲': {
        '中国': {
            '北京',
            '上海',
            '广州',
        },
        '日本': {
            '东京',
            '大板',
            '名古屋',
        }
    },
    '欧洲': {
        '法国',
        '荷兰',
    },
    '美洲': {
        '美国': {
            '纽约',
            '洛杉矶',
            '休斯顿',
        }
    },
}

def framework(A='',B='',C=''):
    os.system('cls')
    print('''
**************************************************
        选 择 您 想 查 看 的 内 容 序 号

        洲：%s      国家：%s      城市：%s
**************************************************
''' % (A,B,C))
def input_handle(s):
    if str.isdigit(s):
        s = int(s)
    return s

def continent_show(continent_list):
    global A_NAME
    global B_NAME
    global C_NAME
    global FLAG_A
    continent_dict = {}
    for i,j in enumerate(continent_list,1):
        continent_dict[i] = j
        print('%d.%s'%(i,j))
    print('=================================================')
    print('q = exit')
    continent_index = input('请输入编号或者洲名称： ')
    #if len(continent_index) != 0:
    if len(continent_index) != 0:
        continent_index = input_handle(continent_index)
    #print(type(continent_index))                      # 上面input输入的数字会被识别为str,所以要加一部格式化操作
    if continent_index == 'q':
        sys.exit(1)
    elif continent_index in continent_dict.keys():
        A_NAME = continent_dict[continent_index]
    elif continent_index in continent_dict.values():
        A_NAME = continent_index
    else:
        A_NAME = ''

    while A_NAME:
        if type(id_db[A_NAME]) is dict:
            country_show(A_NAME)
            if FLAG_A == 'b':
                break
        else:
            show(A_NAME)
            time.sleep(5)
            break

    else:
        print("输入错误，请重新输入...")
        time.sleep(2)



def country_show(country_name):
    global A_NAME
    global B_NAME
    global C_NAME
    global FLAG_A

    country_name = ''
    country_list = id_db[A_NAME]
    country_dict = {}
    print('=================================================')
    for i,j in enumerate(country_list,1):
        country_dict[i] = j
        print('%d.%s'%(i,j))
    print('=================================================')
    print('q = exit  b = back')

    country_index = input("请输入国家编或名称： ")
    if len(country_index) != 0:
        country_index = input_handle(country_index)
    if country_index == 'q':
        sys.exit(2)
    elif country_index == 'b':
        (A_NAME,B_NAME,FLAG_A) = ('','','b')
        return
    elif country_index in country_dict.keys():
        B_NAME = country_dict[country_index]
    elif country_index in country_dict.values():
        B_NAME = country_index
    else:
        pass







def show(A_NAME='',B_NAME='',C_NAME=''):
    print('''
******************************************************
                   %s,%s,%s  欢迎你！
******************************************************
    '''% (A_NAME,B_NAME,C_NAME))









continent_list = id_db.keys()


A_NAME = ''                   # A代表第一层菜单
B_NAME = ''                   # B代表第二层菜单
C_NAME = ''                   # C代表第三层菜单
FLAG_A = ''
FLAG_B = ''


while True:
    framework(A_NAME,B_NAME,C_NAME)
    continent_show(continent_list)


