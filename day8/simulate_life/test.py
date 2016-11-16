# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import sys

import time


class Person(object):
    assets = 0  # 初始化资产为 0 元

    lover = None  # 恋爱对象

    love_status = None  # 恋爱状态

    role_font_color = {'rich': 32, 'poor': 34, 'beauty': 35}  # 设置不同角色谈话字体颜色

    def __init__(self, name, age, sex, role):

        self.name = name

        self.age = age

        self.sex = sex

        self.role = role

        if self.role == 'rich':

            self.assets += 1000000

        elif self.role == 'poor':

            self.assets += 5000

        elif self.role == 'beauty':

            self.assets += 5000

    def talk(self, msg, tone='normal'):

        '''

        正常的交谈，字体颜色为

        :param msg:

        :param tone:

        :return:

        '''

        if tone == 'angry':

            for s in msg:
                sys.stdout.write('\033[31;1m%s\033[0m' % s)

                sys.stdout.flush()

                time.sleep(0.1)

            sys.stdout.write('\n')

        else:

            for s in msg:
                sys.stdout.write('\033[%d;1m%s\033[0m'

                                 % (self.role_font_color[self.role], s))

                sys.stdout.flush()

                time.sleep(0.1)

            sys.stdout.write('\n')

    def all_assets(self, money, action):

        '''

        个人拥有的资产值,计算赚的钱与花的钱

        :param: money  钱的数目

        :param: action  赚到或者花费

        '''

        if action == 'earn':

            self.assets += money

            print('\033[32;1m%s赚得了 %s 元!现在拥有 %s 元\033[0m'

                  % (self.name, money, self.assets))

        elif action == 'cost':

            self.assets -= money

            print('\033[31;1m%s花费了 %s 元! 现在还剩余 %s 元\033[0m'

                  % (self.name, money, self.assets))


def introduce(p1, r1, b1):
    '''

    初始化人物角色，开场自我介绍。

    :param p1:  一个穷人角色

    :param r1: 一个富人角色

    :param b1: 一个美女角色

    :return:None

    '''

    for i in range(1, 101):
        print('游戏加载中：| %-25s | \033[31;1m%3d%%\033[0m' % ('>' * (i // 4), i), end='\r')  # 字符串中表示%，要用双%%才行

        time.sleep(0.05)

    print('')

    print('*' * 50)

    print('\033[33;1m 欢迎登陆模拟职场人生游戏 \033[0m'.center(50))

    print('*' * 50)

    print('游戏人物简介：')

    p1.talk('[%s]: 嗨，我叫小明，今年%d岁，一个贫穷的男孩。我讨厌贫穷，希望通过努力工作来改变自己的生活！'

            % (p1.name, p1.age))

    r1.talk('[%s]: 嗨，我叫小富，今年%d岁，一个富二代的男孩。我有车有房，喜欢泡漂亮的姑娘，有钱让我随心所欲！'

            % (r1.name, r1.age))

    b1.talk('[%s]: 嗨，我叫小丽，今年%d岁，一个漂亮的女孩。虽然我拥有的钱不多，但是我很漂亮。我不希望永远到贫穷下去！'

            % (b1.name, b1.age))


def show_induction():
    '''

    入职工作介绍

    :return:

    '''

    print('-' * 50)

    print('第一章：入职公司'.center(50))

    print('-' * 50)

    print('小明和小丽是大学恋人，毕业后一起入职同一家公司。'

          '\n他俩埋头苦干的工作，都想努力赚多点钱。'

          '\n两年都过去了，他们赚到了多少钱呢？')

    p1.all_assets(40000, 'earn')

    b1.all_assets(35000, 'earn')

    time.sleep(1)


def show_feelings():
    '''

    感情出现信任危机

    :return:

    '''

    print('-' * 50)

    print('第二章：感情危机'.center(50))

    print('-' * 50)

    b1.talk('[%s]: 小明，我们恋爱那么久，都没车没房，生活怎么过啊？' % b1.name)

    p1.talk('[%s]: 小丽，我们一起奋斗，以后生活肯定会过得更好的！' % p1.name)

    b1.talk('[%s]: 不，现在我想结束这样的生活。小富对我很好，他有车有房，能给与我很多，所以我想他在一起！'

            % b1.name, 'angry')

    r1.talk('[%s]: 对，我是真心爱小丽的，你这么穷，就别做美梦了吧！' % r1.name)

    p1.talk('[%s]: 小丽，我们在一起很开心啊！小富不是表面上那么好的人。' % p1.name)

    b1.talk('[%s]: 那不是我要的生活，我们分手吧！' % b1.name, 'angry')

    p1.talk('[%s]: 给我考虑3天时间，到时候你我重新做决定吧！' % p1.name)

    b1.talk('[%s]: 好吧，就给你3天时间！' % b1.name)

    time.sleep(1)


def break_up():
    '''

    poor 角色与 beauty 角色选择分手，最终结局。

    :return:

    '''

    print('-' * 50)

    print('第三章：分手结局'.center(50))

    print('-' * 50)

    p1.talk('[%s]: 小丽，你既然决定要分手，好吧，那就分吧！' % p1.name)

    p1.talk('[%s]: 总有一天你会后悔的，等着瞧' % p1.name, 'angry')

    b1.talk('[%s]: 小富，我们走！' % b1.name, 'angry')

    print('伤心过后的小明，通过参加Python培训，他最终当上IT总监。他也买有车、房了。')

    p1.all_assets(5000000, 'earn')

    print('有一天，小明开车路过的大街上，看到两个人吵架，挡住前方的路。他下车看看情况，让他大吃一惊！')

    p1.talk('[%s]: 你们让一下，不要挡着路！让我开车过去' % p1.name, 'angry')

    b1.talk('[%s]: 小明，我是小丽啊，他就是小富。' % b1.name, )

    print('此时的他们，小富因为花心，花光了所有钱。小丽也因为小富也变得贫穷。因为钱，他们已经分手吵架了。')

    p1.talk('[%s]: 你们的报应啊，早知道这样，何必当初呢！' % p1.name)

    b1.talk('[%s]: 小明，我想再次和你在一起，好吗？' % b1.name, )

    b1.talk('[%s]: 别做梦啦，当初你因为钱而跟了小富，现在是回不来头了。说完开着车走了！' % b1.name, 'angry')

    print('最终小丽不再美丽了，变回了穷女孩。而小富也因为过度玩乐，花光所有的钱，变成穷光蛋！')

    print('\033[31;1m  剧 终  \033[0m'.center(50, '*'))


def together():
    '''

    角色poor 和 beauty 选择在一起，最终结局

    :return:

    '''

    print('-' * 50)

    print('第三章：完美结局'.center(50))

    print('-' * 50)

    print('小明和小丽选择了在一起，永不分开！')

    p1.talk('[%s]: 小丽，你终于想通啦，我们才是天生一对！' % p1.name)

    b1.talk('[%s]: 嗯，即使小富有车有房，但是他整天去泡多个姑娘，这种人不值得在一起！' % b1.name)

    b1.talk('[%s]: 我们通过自己的努力，也会赚到很多钱的！' % b1.name)

    r1.talk('[%s]: 小丽，我不是你说的那样的人，那些姑娘是主动约我的，我也无耐啊！' % r1.name)

    b1.talk('[%s]: 小明，我们一起辞职吧！我不想在看到小富！' % b1.name, 'angry')

    p1.talk('[%s]: 好，我们一起努力，终有收获的！' % p1.name)

    print('小明和小丽通过自己的努力，最终也买车买房p了。而小富因为整天泡妞，拥有的钱都花光了，变成了穷屌丝！')

    print('\033[31;1m  剧 终  \033[0m'.center(50, '*'))


def choose():
    '''

    情侣矛盾部分，可选择‘分手’ 或者 ‘在一起’

    :return:

    '''

    print('-' * 50)

    print('约定的3天时间到了，你我重新选择:\033[31;1m1 分手 2 在一起\033[0m')

    while True:

        choose1 = input('小明，请选择 1 或者 2 ：').strip()

        if choose1 == '':
            continue

        choose2 = input('小丽，请选择1或者2：').strip()

        if choose2 == '':
            continue

        if choose1 in ['1', '2'] and choose2 in ['1', '2']:

            if choose1 == '2' and choose2 == '2':  # 双方决定在一起

                together()

                break

            elif choose1 == '1' or choose2 == '1':  # 任意一方选择分手

                break_up()

                break

        else:

            print('你选择的不正确，请重新选择！')


if __name__ == '__main__':
    p1 = Person('小明', 25, 'Male', 'poor')

    r1 = Person('小富', 24, 'Male', 'rich')

    b1 = Person('小丽', 22, 'Female', 'beauty')

    introduce(p1, r1, b1)  # 角色自我介绍

    show_induction()  # 入职公司部分

    show_feelings()  # 感情危机部分

    choose()