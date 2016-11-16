# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import configparser
from lib import module
from config import setting


def register():
    print('''\033[32;0m
- - - - - - - - - - - - - - - - - - - -

    大型魔幻巨制 ---<<诛仙Online>>

- - - -  - - - - - - - - - - - - - - - -
    \033[0m''')
    while True:
        player_name = input('请输入角色名称： \n>> ')
        if not player_name:
            continue
        player_gender = input('请选择角色性别：\033[32;0m1、『男』\033[0m \033[35;0m2、『女』\033[0m \n>>')
        if player_gender == '1':
            character_obj = module.Character(name=player_name, gender='男', color_num=32)
            break
        elif player_gender == '2':
            character_obj = module.Character(name=player_name, gender='女', color_num=32)
            break
    return character_obj


def main():
    character_obj = register()
    character_npc = module.Character(name='青云门首座田不易', gender='男', color_num=35)
    character_obj.story_show('session1', 's1')
    character_obj.story_show('session1', 's2')
    character_obj.story_show('session1', 's3')
