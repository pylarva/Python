#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render


class DocumentListView(View):
    """
    cmdb 更新说明文档
    """
    def dispatch(self, request, *args, **kwargs):
        return super(DocumentListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, nid):
        if nid == "1":
            return render(request, 'document_1.html')
        elif nid == "2":
            return render(request, 'document_2.html')


