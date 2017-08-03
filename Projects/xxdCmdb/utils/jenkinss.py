# !/usr/bin/env python
# -*- coding:utf-8 -*-
import jenkins
from conf import jenkins_config


def build_obj(build_name, pkg_url, git_url, git_branch):
    server = jenkins.Jenkins(jenkins_config.server_url, username=jenkins_config.user_name, password=jenkins_config.api_token)
    ret = server.build_job(name='template-tomcat', parameters={'pkgUrl': pkg_url, 'git_url': git_url, 'branch': git_branch})
    return ret

