# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import time
from src import atm_main

SHOPPING_CAR = []


def car(SHOPPING_CAR):
    if SHOPPING_CAR:
        print('  购物车  '.center(40, '-'))
        print('商品       数量       总价')
        sum_pay = 0
        for item in SHOPPING_CAR:
            print('%(name)-10s %(nums)-10d %(sum)-10d' % item)
            sum_pay += item['sum']
        print('总消费 \033[31;0m%d\033[0m,是否结算? Y|N' % sum_pay)
        deal = input('>> ')
        if deal.upper() == 'Y':
            atm_main.shopping_withdraw(SHOPPING_CAR, sum_pay)
    else:
        print('购物车为空...')


def main():
    exit_flag = False

    # 第一层循环打印菜单
    while not exit_flag:
        print('  购物商城  '.center(40, '-'))
        product_dict = {
            '家电类': {'乐视TV': 1999, '海尔冰箱': 1500},
            '数码类': {'Mac Pro': 9888, 'iphone': 5888},
            '服饰类': {'Adidas': 399, 'POLO': 299},
            '汽车类': {'Tesla': 888888, 'TOYOTA': 200000},
        }
        # 分类列表
        product_first = {}
        for k, v in enumerate(product_dict):
            product_first[k] = v
            print('%d. %s' % (k, v))

        select_one = input('输入编号 [q退出 c购物车]： ')
        if select_one.upper() == 'C':
            car(SHOPPING_CAR)
        if select_one.upper() == 'Q':
            print('退出商城成功！')
            time.sleep(1)
            break
        if select_one.isdigit():
            select_one = int(select_one)
            if select_one in product_first:
                select_name = product_first[select_one]
                product_second = {}
                print('-------- HOME > %s --------' % product_first[select_one])
                for i, j in enumerate(product_dict[select_name]):
                    product_second[i] = j
                    print('%d. %s %d' % (i, j, product_dict[select_name][j]))

                while not exit_flag:
                    select_two = input('选择商品[Q退出 B返回上一层]： ')
                    if select_two.upper() == 'Q':
                        exit_flag = True
                        break
                    if select_two.upper() == 'B':
                        break
                    if select_two.isdigit():
                        select_two = int(select_two)
                        if select_two in product_second:
                            print(product_second)
                            num = input('数量：')
                            num = int(num)
                            add_car = {
                                'name': product_second[select_two],
                                'nums': num,
                                'sum': num * product_dict[select_name][product_second[select_two]]
                            }
                            SHOPPING_CAR.append(add_car)
                            print(SHOPPING_CAR)

if __name__ == '__main__':
    main()