# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import configparser
import sys
import time
from config import setting


class Character:
    """
    游戏创建人物类 包含构造方法 定义对话输出屏幕函数 做任务加钱加经验函数
    """
    npc = '[大竹峰首座]田不易'

    def __init__(self, name, color_num):
        self.name = name
        self.color_num = color_num
        self.skill = ''
        self.level = 0
        self.asset = 0

    def story_show(self, session_num, key_num):
        """
        游戏背景介绍输出
        :param session_num:
        :param key_num:
        :return:
        """
        # 仅读取游戏背景介绍会话 区分 人物名 和 词条为两种不同颜色显示
        config = configparser.ConfigParser()
        config.read(setting.text_file, encoding='utf-8')
        session = config.get(session_num, key_num)
        player_name = str(self.name)
        for s in session:
            sys.stdout.write('\033[35;1m%s\033[0m' % s)
            sys.stdout.flush()
            if s == '[':
                for ss in player_name:
                    sys.stdout.write('\033[31;1m%s\033[0m' % ss)
                    sys.stdout.flush()
            time.sleep(0.15)
        print('\n')

    def session_show(self, session_num, key_num):
        """
        游戏人物会话输出
        :param session_num:
        :param key_num:
        :return:
        """
        # 使用configparser函数读取 db.text 会话内容格式化输出到屏幕
        config = configparser.ConfigParser()
        config.read(setting.text_file, encoding='utf-8')
        session = config.get(session_num, key_num)
        session = session.format(self.name, self.skill)
        for s in session:
            sys.stdout.write('\033[%d;1m%s\033[5m' % (self.color_num, s))
            sys.stdout.flush()
            time.sleep(0.1)
        print('\n')

    def gain_asset(self):
        """
        做任务加钱 升级
        :return:
        """
        self.asset += 5
        self.level += 1

    def upgrade_level(self):
        """
        做耗钱任务 升等级
        :return:
        """
        self.asset -= 10
        self.level += 5
