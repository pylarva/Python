# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import sys
import time


class Person(object):
    rolesflag = {"loser":32,"peri":36,"fat_cat":31}  # 定义输出颜色标示

    def __init__(self,name,age,sex,role,asset):
        self.name = name
        self.age = age
        self.sex = sex
        self.role = role
        self.asset = asset

    def talk(self, msg, tone='normal'):
        '''
        :param msg:交谈的字体颜色定义
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
                sys.stdout.write('\033[%d;1m%s\033[0m' % (self.rolesflag[self.role], s))
                sys.stdout.flush()
                time.sleep(0.1)
            sys.stdout.write('\n')

    def asset_total(self, money, action):
        '''
        角色拥有的资产值,计算赚的钱与花的钱
        :param: money  钱的数目
        :param: action  花费
        '''
        if action == 'earn':
            self.asset += money
            print('\033[32;1m%s赚了 %s 元!资产增加 %s 元\033[0m' % (self.name, money, self.asset))
        elif action == 'cost':
            self.asset -= money
            print('\033[31;1m%s花了 %s 元! 仅剩 %s 元\033[0m' % (self.name, money, self.asset))


def progress_test():
    """
    定义进度条
    """
    bar_length=80
    for percent in range(0, 101):
        hashes = '#' * int(percent/100.0 * bar_length)
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\rLoading: [%s] %d%%"%(hashes + spaces, percent))
        sys.stdout.flush()
        time.sleep(0.05)


def introduce(p1,p2,p3):
    '''
    初始化人物角色，开场介绍。
    :param p1: 屌丝角色
    :param p2: 土豪角色
    :param p3: 美女角色
    :return:None
    '''
    print('')
    print('*' * 150)
    print('\033[31;1m 欢迎登陆模拟人生游戏 \033[0m'.center(150))
    print('*' * 150)

    print('游戏人物简介：')
    p1.talk('[%s]: 我是2B，今年%d岁，我是一个从农村出来的孩子，对未来充满憧憬，虽然穷，但是有个美丽的女朋友一直是我的骄傲！'
            '代言loser' % (p1.name, p1.age))
    p2.talk('[%s]: 我是土豪猫，今年%d岁，一个准官二代。有车有房，身边除了钱就是妹子，生活已经没有多大追求了，除了嗑药，把妹'
            '是我唯一的爱好！代言fat_cat' % (p2.name, p2.age))
    p3.talk('[%s]: 我是美丽，今年%d岁，人如其名，除了好看以外还有着36D的骄傲，那个谁谁谁都可以演《美人鱼》一炮而红，我不甘心'
            '，我要奢侈生活！代言peri' % (p3.name, p3.age))


def show_story():
    '''
    故事背景介绍
    :return:
    '''
    print('-' * 150)
    print('第一章：故事背景'.center(150))
    print('-' * 150)
    print('2B和美丽是发小，从初中开始幼稚恋一直到大学毕业，毕业后一起到大北京闯荡江湖。'
          '\n2B通过自己的努力奋斗，终于找到了一份8000块的工作，美丽也找到一份5000块的工作'
          '\n通过两人的努力奋斗，小两口终于有点小积蓄了，可是他们发现房价越来越高了，在看看自己的积蓄才这么一点点：')
    p1.asset_total(20000, 'earn')
    p3.asset_total(10000, 'earn')
    print('2B发现了美丽的不爽，心想：不如先把婚给结了，然后再考虑未来，否则媳妇儿跑了，再找就麻烦了，于是开始准备求婚计划了.')
    time.sleep(0.5)


def show_crisis():
    '''
    感情出现信任危机
    :return:
    '''
    print('-' * 150)
    print('第二章：求婚显危机'.center(150))
    print('-' * 150)
    p1.talk('[%s]: 美丽，我们一起了这么多年，我的真心天地可鉴，请嫁给我吧！' % p1.name)
    p3.talk('[%s]: 2B，我们恋爱那么久，没车没房，买个爱马仕的包包，我想都不敢想，以后的生活怎么过啊？' % p3.name)
    p1.talk('[%s]: 美丽，我们一起努力，以后生活肯定会过得更好的！' % p1.name)
    p3.talk('[%s]: 我受够了这样的生活，放弃吧！猫对我很好，我想我们该结束了'% p3.name)
    p2.talk('[%s]: 对，我对美丽是真心的，你这么穷，就别瞎胡闹了！' % p2.name)
    p1.talk('[%s]: 美丽，你说的是真的吗，你爱他吗？' % p1.name)
    p3.talk('[%s]: 我不管，我只想过我要的生活，我们over吧' % p3.name,)
    p1.talk('[%s]: 给我点时间想想吧，到时候我们再做决定！' % p1.name)
    p3.talk('[%s]: 好吧，就给你1天时间！' % p3.name)
    time.sleep(0.5)


def choose():
    """
    用户交互，做出感情决定
    """
    print('-' * 150)
    print('约定的时间到了，开始选择:  \033[31;1m1 不答应 2 答应\033[0m')
    while True:
        one = input('2B，请选择 1 或者 2 ：').strip()
        if one == '':
            continue
        two = input('美丽，请选择1或者2：').strip()
        if two == '':
            continue
        if one in ['1', '2'] and two in ['1', '2']:
            if one == '2' and two == '2':
                together()
                break
            elif one == '1' or two == '1':
                separate()
                break
        else:
            print('你不按套路出牌啊，说好的选择1和2，你偏选3，告诉你选择3等于重来，哈哈', 'angry')


def together():
    '''
    角色2B 和 美丽 选择在一起，最终结局输出
    :return:
    '''
    print('-' * 150)
    print('第三章：在一起后结局'.center(150))
    print('-' * 150)
    print('美丽回心转意，答应了2B的求婚，两人最终在一起！')
    p1.talk('[%s]: 美丽，你终于想通啦，我们才是门当户对啊！' % p1.name)
    p3.talk('[%s]: 嗯，即使猫有车有房，但是他整天去泡妞娘，还吸毒，这种人太不靠谱了！' % p3.name)
    p3.talk('[%s]: 我们通过自己的努力，也会有房有车有爱马仕的！' % p3.name)
    p2.talk('[%s]: 美丽，我不是你说的那样的人，你误会了！' % p2.name)
    p3.talk('[%s]: 2B我们离开这里吧，我不想再见到他了' % p3.name)
    p1.talk('[%s]: 好，我们一起走！' % p1.name)
    print('2B和美丽离开了大北京，经过若干年的努力也有房有车了，猫因为吸毒久了，最终挂了！')
    print('\033[31;1m  剧 终  \033[0m'.center(150, '*'))


def separate():
    '''
    角色2B 和 美丽 选择在不一起，最终结局输出
    :return:
    '''
    print('-' * 150)
    print('第三章：2B失败了，美丽和高富帅走了'.center(150))
    print('-' * 150)
    p1.talk('[%s]: 美丽，你真狠心，真的能忘记过去吗？' % p1.name)
    p3.talk('[%s]: 我不能，但是我能改变现在... ...' % p3.name, 'angry')
    p1.talk('[%s]: 希望你不要后悔' % p1.name)
    p3.talk('[%s]: 2B你也别太难过，找个好人就嫁了吧。猫，我们走吧！' % p3.name, 'angry')
    print('伤心过后的2B，参加Python培训，最终当上CIO，也买车买房了。（怎么可能呢？哈哈）')
    print('当了CIO的2B在公司门口唱了一首《没有理想的人不伤心》一炮走红，老板为了公司打广告一口气给了2B一大笔奖金：')
    p1.asset_total(5000000, 'earn')
    print('终有一天，2B在五星级酒店吃饭看到一个服务员，当场惊呆了！')
    p1.talk('[%s]: 你怎么会在这里？' % p1.name, 'angry')
    p3.talk('[%s]: 猫去年因为吸毒挂了，留下了一堆债务还有我... ...' % p3.name, )
    p1.talk('[%s]: 造孽啊，早知今日，何必当初呢！' % p1.name, 'angry')
    p3.talk('[%s]: 2B，你能帮帮我吗？' % p3.name, )
    p1.talk('[%s]: 100W如何？' % p1.name, 'angry')
    p3.talk('[%s]: 我不要钱，我只想给肚子里的孩子找个爹' % p3.name)
    p1.talk('[%s]: 别做梦啦，把孩子打掉吧，虽然他是无辜的，但也成不了富二代了！' % p1.name, 'angry')
    print('最终2B潇洒的丢了50W，扬长而去... ...美丽最终选择离开了大北京，回到老家继续苦逼的生活！')
    print('\033[31;1m  剧 终  \033[0m'.center(150, '*'))

if __name__ == "__main__":
    p1 = Person("loser",22,"Male","loser",8000)
    p2 = Person("fat_cat",31,"Male","fat_cat",500000)
    p3 = Person("peri",21,"Female","peri",5000)
    progress_test()
    introduce(p1,p2,p3)
    show_story()
    show_crisis()
    choose()