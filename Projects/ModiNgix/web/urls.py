# !/usr/bin/env python
# -*- coding:utf-8 -*-
import web.views
from django.conf.urls import url
from web.views import nginx


urlpatterns = [
    url(r'^index/', nginx.IndexView.as_view()),
    url(r'^nginx/', nginx.NginxView.as_view()),
]
