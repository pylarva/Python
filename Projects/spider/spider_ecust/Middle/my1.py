# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse


class Row1(MiddlewareMixin):
    def process_request(self, request):
        print('request_row_1')

    def process_view(self, request, view_func, view_func_args, view_func_kwargs):
        print('view_row_1')

    def process_response(self, request, response):
        print('process_row_1')
        return response