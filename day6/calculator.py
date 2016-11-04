# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import re

s = '8*12 + (6-(5*6 - 2)/77+2)*(3-7)+8'
# s1 = '8*-1(2+-*7/)/7'
# s = re.sub('\s', '', s)
# print(s)
#
# if re.search('[^0-9 *+-./]', s):
# if re.search('\(', s1):
#     print('ok')
# else:
#     print('no')

# a = 'a(bca)d'
# print(re.search('\([0-9 *+-/]+\)', s).group())


def deal_bracket(exp):
    exp = exp[0]
    print(exp)
    print('zzzzzzzzzzzzzzz')
    # 处理乘除
    while re.search('\d+[*/]\d+', exp):
        # f得到括号内的第一个乘除表达式
        f = re.search('\d+[*/]\d+', exp).group()
        print(f)
        exp_before = re.split('(\d+[*/]\d+)', exp, 1)[0]
        exp_back = re.split('(\d+[*/]\d+)', exp, 1)[2]
        print(111111111111)
        print(exp_before)
        print(exp_back)
        # 如果是乘法
        if re.match('\d+[*]\d+', f):
            t = re.split('[*]', f)
            print(t)
            res = int(t[0]) * int(t[1])
            exp = exp_before + str(res) + exp_back
            print(exp)
            continue
        elif re.match('\d+[/]\d+', f):
            t = re.split('[/]', f)
            print(t)
            res = int(t[0]) / int(t[1])
            res = int(res)
            exp = exp_before + str(res) + exp_back
            print(exp)
            continue

    while re.search('\d+[+-]\d+', exp):
        # f得到括号内的第一个加减表达式
        f = re.search('\d+[+-]\d+', exp).group()
        print(f)
        exp_before = re.split('(\d+[+-]\d+)', exp, 1)[0]
        exp_back = re.split('(\d+[+-]\d+)', exp, 1)[2]
        print(111111111111)
        print(exp_before)
        print(exp_back)
        # 如果是加法
        if re.match('\d+[+]\d+', f):
            t = re.split('[+]', f)
            print(t)
            res = int(t[0]) + int(t[1])
            exp = exp_before + str(res) + exp_back
            print(exp)
            continue
        elif re.match('\d+[-]\d+', f):
            t = re.split('[-]', f)
            print(t)
            res = int(t[0]) - int(t[1])
            res = int(res)
            exp = exp_before + str(res) + exp_back
            print(exp)
            continue

    return exp


def run(s):

    while re.search('\(', s):
        s_before = re.split('\(([0-9 *+-/]+)\)', s, 1)[0]
        s_back = re.split('\(([0-9 *+-/]+)\)', s, 1)[2]
        bracket = re.search('\(([0-9 *+-/]+)\)', s).groups()
        print(bracket)
        result = deal_bracket(bracket)
        s = s_before + result + s_back
        continue

    bracket = re.search('(.*)', s).groups()
    result = deal_bracket(bracket)

    print(result)

if __name__ == '__main__':
    # s = '8*12'
    s = '8*12 + (6-(15*6*2-2/1)/77+2)*(9-7)+8'
    # s = '8+2-(8*2+(8/2+2*(15*6/9+1)))'
    # s = '1-2*-30/-12*(-20+200*-3/-200*-300-100)'
    s = re.sub('\s', '', s)
    run(s)