# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 计算过程
# s1 = 1 + (4/-2-(-4/2+4-2*-1))
# s2 = 1 + (4/-2-(-2+4-2*-1))
# s3 = 1 + (4/-2-(-2+4--2))
# s4 = 1 + (4/-2-(-2+4+2))
# s5 = 1 + (4/-2-4)
# s6 = 1 + -6
# s7 = -5

import re


def symbols_replace(exp):
    """
    替换计算过程中得到的多余计算符号
    :param exp:
    :return:
    """
    exp = exp.replace('++', '+')
    exp = exp.replace('+-', '-')
    exp = exp.replace('--', '+')
    exp = exp.replace('-+', '-')
    return exp


def deal_bracket(exp):
    """
    得到括号最内层内容后 计算里面的加减乘除
    :param exp:
    :return:返回计算结果
    """
    exp = exp[0]

    # 处理乘除
    while re.search('-*\d+[*/]-*\d+', exp):
        # f得到括号内的第一个乘除表达式
        f = re.search('\d+[*/]-*\d+', exp).group()
        exp_before = re.split('(\d+[*/]-*\d+)', exp, 1)[0]
        exp_back = re.split('(\d+[*/]-*\d+)', exp, 1)[2]

        # 如果是乘法
        if re.search('\d+[*]-*\d+', f):
            t = re.split('[*]', f)
            res = int(t[0]) * int(t[1])
            exp = exp_before + str(res) + exp_back
            exp = symbols_replace(exp)
            continue

        # 如果是除法
        elif re.search('\d+[/]-*\d+', f):
            t = re.split('[/]', f)
            res = int(t[0]) / int(t[1])
            res = int(res)
            exp = exp_before + str(res) + exp_back
            exp = symbols_replace(exp)
            continue

    # 处理加减
    while re.search('\d+[+-]', exp):
        # f得到括号内的第一个加减表达式
        exp = symbols_replace(exp)
        f = re.search('-*\d+[+-]\d+', exp).group()
        exp_before = re.split('(-*\d+[+-]\d+)', exp, 1)[0]
        exp_back = re.split('(-*\d+[+-]\d+)', exp, 1)[2]

        # 如果是加法
        if re.search('-*\d+[+]\d+', f):
            t = re.split('[+]', f)
            res = int(t[0]) + int(t[1])
            exp = exp_before + str(res) + exp_back
            continue

        # 如果减法
        elif re.search('-*\d+[-]\d+', f):
            # 实在不知道怎么分割 '-2-4' 来计算
            if re.match('-', f):
                res = eval(f)
            else:
                t = re.split('[-]', f)
                res = int(t[0]) - int(t[1])
            res = int(res)
            exp = exp_before + str(res) + exp_back
            continue

    return exp


def run(s):
    """
    第一层循环：得到最里层括号内的表达式 交给计算函数 deal_bracket 计算
    :param s:
    :return:
    """
    while re.search('\(', s):
        # 分割表达式：前部分 + （最里层表达式） + 后部分
        s_before = re.split('\(([0-9 *+-/]+)\)', s, 1)[0]
        s_back = re.split('\(([0-9 *+-/]+)\)', s, 1)[2]
        bracket = re.search('\(([0-9 *+-/]+)\)', s).groups()
        result = deal_bracket(bracket)
        # 计算完里层表达式后重新拼接为一个新的表达式 再次循环计算
        s = s_before + result + s_back
        continue

    # 如果表达式内没有括号 直接计算
    bracket = re.search('(.*)', s).groups()
    result = deal_bracket(bracket)

    print(result)

# 主程序输入表达式
if __name__ == '__main__':
    # s = '8*12'
    # s = '8*12 + (6-(15-6*-2-(-2/1*3-1))/77+2)*(9-7)+8'
    # s = '8+2-(8*2+(8/2+2*(15*6/9+1)))'
    # s = '1-2*-30/-12*(-20+200*-3/-200*-300-100)'
    # s = '1 + (4/-2-(-4/2+4-2*-1))'
    while True:
        s = input('请输入表达式： ')
        if s:
            s = re.sub('\s', '', s)
            run(s)

