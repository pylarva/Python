# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import sys
import time
from lib import module


def register():
    """
    创建角色
    :return:
    """
    print('''\033[32;0m
- - - - - - - - - - - - - - - - - - - -

    大型魔幻巨制 ---<<诛仙Online>>

- - - -  - - - - - - - - - - - - - - - -
    \033[0m''')
    while True:
        player_name = input('请输入角色名称： \n>> ')
        if not player_name:
            continue
        character_obj = module.Character(name=player_name, color_num=32)
        break
    return character_obj


def select_skill(character_obj, character_npc2):
    """
    游戏第二章节：选玄术
    :param character_obj:
    :param character_npc2:
    :return:
    """
    character_obj.story_show('session2', 's0')
    time.sleep(2)
    character_obj.session_show('session2', 's1')
    character_npc2.session_show('session2', 's2')
    character_obj.session_show('session2', 's3')
    character_npc2.session_show('session2', 's4')
    character_obj.session_show('session2', 's5')
    character_npc2.session_show('session2', 's6')
    while True:
        print('''\033[36;0m
        1、诛仙剑阵
        2、神剑御雷真诀
        3、御岩术
        4、清风决
        \033[0m''')
        skill_dict = {'1': '诛仙剑阵', '2': '神剑御雷真诀', '3': '御岩术', '4': '清风决'}
        select_num = input('选择 >> ')
        if select_num == '1':
            character_obj.skill = '诛仙剑阵'
            character_obj.session_show('session3', 's1')
            character_npc2.session_show('session3', 's2')
            break
        elif select_num == '2':
            character_obj.skill = skill_dict[select_num]
            character_obj.session_show('session4', 's1')
            character_npc2.session_show('session4', 's2')
            break
    return character_obj


def exercise(character_obj, character_npc1):
    """
    游戏第三章节：修炼
    :param character_obj:
    :param character_npc1:
    :return:
    """
    character_obj.story_show('session5', 's1')
    character_npc1.session_show('session5', 's2')
    character_obj.session_show('session5', 's3')
    while True:
        print('\033[35;0m{} 当前修炼技能：[{}] 等级：[{}],金钱:[{}]\033[0m'.format(character_obj.name, character_obj.skill,
                                               character_obj.level, character_obj.asset))
        print('''\033[36;0m
        1、砍柴挑水(金钱+5 等级+1)
        2、下山收妖(金钱-10 等级+5)
        3、勇夺诛仙剑(需要等级>=10)
        \033[0m''')
        select_num = input('选择 >> ')
        if select_num == '1':
            character_obj.gain_asset()
            character_npc1.session_show('session5', 's4')
            continue
        elif select_num == '2':
            if int(character_obj.asset) < 10:
                character_npc1.session_show('session5', 's5')
                character_npc1.session_show('session5', 's8')
                time.sleep(2)
                continue
            else:
                character_obj.upgrade_level()
                character_npc1.session_show('session5', 's6')
                continue
        elif select_num == '3':
            if int(character_obj.level) < 10:
                character_npc1.session_show('session5', 's7')
                character_npc1.session_show('session5', 's8')
                time.sleep(2)
                continue
            else:
                character_npc1.session_show('session5', 's9')
                return character_obj


def main():
    """
    游戏主函数
    :return:
    """
    # 用户创建一个角色
    character_obj = register()
    # 自动创建两个NPC
    character_npc1 = module.Character(name='青云门首座田不易', color_num=36)
    character_npc2 = module.Character(name='田灵儿', color_num=35)
    # 游戏第一章节：初入青云门
    character_obj.story_show('session1', 's1')
    character_obj.story_show('session1', 's2')
    time.sleep(2)
    character_npc1.session_show('session1', 's3')
    character_obj.session_show('session1', 's4')
    character_npc2.session_show('session1', 's5')
    character_npc1.session_show('session1', 's6')
    character_obj.session_show('session1', 's7')
    character_npc1.session_show('session1', 's8')
    character_obj.session_show('session1', 's9')
    character_npc2.session_show('session1', 's10')
    # 游戏第二章节：选玄术
    character_obj = select_skill(character_obj, character_npc2)
    time.sleep(2)
    # 游戏第三章节：修炼闯关
    exercise(character_obj, character_npc1)
    print(' \033[32;0m----------------------  通关  -----------------------\033[0m')




