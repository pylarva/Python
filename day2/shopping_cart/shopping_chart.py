#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import sys, time


def shopping_home(user_name,salary):
    FLAGE_A = True
    shopping_car = []
    while FLAGE_A:
        product_dict = {
            '家电类':[('乐视TV',1999),('海尔冰箱',1500)],
            '数码类':[('Mac Pro',9888),('iphone',5888)],
            '服饰类':[('Adidas',399),('POLO',299)],
            '汽车类':[('Tesla',888888),('TOYOTA',200000)],
        }
        print(' PRODUCT LIST '.center(50, '-'))
        product_type = {}
        for i,j in enumerate(product_dict.keys()):
            product_type[i] = j
            print('%d.%s'% (i,j))
        print('-'.center(50,'-'))
        user_select = input('请选择商品类型： ')
        if user_select.isdigit():
            user_select = int(user_select)
            if user_select in product_type.keys():
                type_name = product_type[user_select]
                while type_name != 0:
                    for item in enumerate(product_dict[type_name]):
                        index = item[0]
                        p_name = item[1][0]
                        p_price = item[1][1]
                        print(index,'.',p_name,p_price)
                    user_choice = input('[q=退出,c=查看购物车,b=返回上一层] 您想购买什么?: ')
                    if user_choice.isdigit():
                        user_choice = int(user_choice)
                        if user_choice < len(product_dict[type_name]):
                            p_item = product_dict[type_name][user_choice]
                            num = input('请输入您要购买的数量： ')
                            if num.isdigit():
                                num = int(num)
                                if p_item[1]*num <= salary:
                                    shopping_car.append((p_item[0],num,p_item[1]))
                                    salary -= p_item[1]*num
                                    print('Added %s into shopping car successful,you balance is %s...'% (p_item,salary))
                                    continue
                                else:
                                    user_charge = input('You balance is %s,cannot afford this,do you want recharge? Y|N'% salary)
                                    if user_charge == 'y' or user_charge == 'Y':
                                        recharge(salary)
                                        continue

                    elif user_choice == 'c':
                        show_shoppingcar(shopping_car)
                    elif user_choice == 'q':
                        show_shoppingcar(shopping_car)
                        print('谢谢光临，bey...')
                        sys.exit()
                    elif user_choice == 'b':
                        break
        else:
            print('输入错误,请重新输入...')
            time.sleep(1)


def show_shoppingcar(shopping_car):
    print('您购物车里已购商品如下： ')
    print('商品 数量 价格 总价')
    for m, n in enumerate(shopping_car):
        print('%d.%s %s * %s 【%d】' % (m, n[0], n[1], n[2], (n[1] * n[2])))
    print('_'.center(50, '_'))


def recharge(salary):
    exit_flag = False
    while exit_flag is not True:
        user_charge = input('请输入您要充值的金额： ')
        if user_charge.isdigit():
            user_charge = int(user_charge)
            salary += user_charge
            print('充值成功，您的当前余额为：%d'% salary)
            break
        else:
            print('输入错误,请重新输入...')
            continue


user_file = open('C:/software/github/Python/day2/shopping_cart/user.txt','r+')
user_list = user_file.readlines()
user_name = input('请输入您的用户名： ')
for user_line in user_list:
    (user,password,salary) = user_line.split()
    salary = int(salary)
    if user == user_name:
        i = 0
        while i < 3:
            passwd = input('请输入密码： ')
            if passwd == password:
                print('\033[32;1m%s\033[0m，欢迎您！您当前余额为 \033[31;1m%d\033[0m...'% (user_name,salary))
                print('正在进入购物页面...')
                time.sleep(1)
                shopping_home(user_name,salary)
            else:
                print('密码错误，还剩%d次机会...'% (2-i))
                i += 1
                continue

print('用户未找到...')
sys.exit()





