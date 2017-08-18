# !/usr/bin/env python
# -*- coding:utf-8 -*-

from repository import models


def menu(request):
    """
    用户自定义菜单
    :param audit_id:
    :param audit_msg:
    :return:
    """
    user = request.session['username']
    group = models.UserProfile.objects.filter(name=user).first().group.name
    print(group)
    if group == 'pm':
        menu_str = '''
                <a id="menu_audit" class="menu-item" href="/audit.html">
                    <i class="fa fa-connectdevelop" aria-hidden="true" style="width: 14px; margin-left: 1px"></i>
                    <span>P M 审核</span>
                </a>
        '''
    elif group == 'develop':
        menu_str = '''
                <a id="menu_apply" class="menu-item" href="/project_list.html">
                    <i class="fa fa-paper-plane-o" aria-hidden="true" style="width: 14px; margin-left: 1px"></i>
                    <span>发布申请</span>
                </a>
                <a id="menu_online" class="menu-item" href="/apply.html">
                    <i class="fa fa-ioxhost" aria-hidden="true" style="width: 14px; margin-left: 1px"></i>
                    <span>申请记录</span>
                </a>
        '''
    else:
        menu_str = ''
    print('====', menu_str)
    return menu_str