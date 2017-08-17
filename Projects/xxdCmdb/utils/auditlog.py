# !/usr/bin/env python
# -*- coding:utf-8 -*-

from repository import models


def audit_log(audit_id, audit_msg):
    """
    记录发布流程审核日志
    :param audit_id:
    :param audit_msg:
    :return:
    """
    models.AuditLog.objects.create(audit_id=audit_id, audit_msg=audit_msg)
    return True