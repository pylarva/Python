#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing
import sys,os

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
    }
}

def framework(A='',B='',C=''):
    os.system('cls')
    print('''
**************************************************
        选 择 您 想 查 看 的 内 容 序 号

        洲：%s      国家：%s      城市：%s
**************************************************
''' % (A,B,C))

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
    continent_index = input('请输入编号或者名称： ')
    #if len(continent_index) != 0:
    if continent_index == 'q':
        sys.exit()
    elif continent_index in continent_dict.keys():
        A_NAME = continent_dict.values()
    elif continent_index in continent_dict.values():
        A_NAME = continent_index
    else:
        A_NAME = ''

    while A_NAME:
        framework(A_NAME,B_NAME,C_NAME)
        if type.(id_db[A_NAME]) is list:
            country_show(A_NAME)





continent_list = id_db.keys()

A_NAME = ''
B_NAME = ''
C_NAME = ''
FLAG_A = ''
FLAG_B = ''


#while True:
framework(A_NAME,B_NAME,C_NAME)
continent_show(continent_list)


