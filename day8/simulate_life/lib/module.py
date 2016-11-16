# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import configparser
import sys
import time
from config import setting


class Character:

    npc = '[大竹峰首座]田不易'

    def __init__(self, name, gender, color_num):
        self.name = name
        self.gender = gender
        self.color_num = color_num

    def story_show(self, session_num, k_num):
        config = configparser.ConfigParser()
        config.read(setting.text_file, encoding='utf-8')
        session = config.get(session_num, k_num)
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

    def session_show(self):

