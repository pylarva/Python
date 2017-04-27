#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from web.service import chart
from django.utils.decorators import method_decorator
from web.service.login import auth_admin


@method_decorator(auth_admin, name='dispatch')
class IndexView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


@method_decorator(auth_admin, name='dispatch')
class CmdbView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(CmdbView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb.html')


class ChartView(View):
    def get(self, request, chart_type):
        if chart_type == 'business':
            response = chart.Business.chart()
        if chart_type == 'dynamic':
            last_id = request.GET.get('last_id')
            response = chart.Dynamic.chart(last_id)
        return JsonResponse(response.__dict__, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(auth_admin, name='dispatch')
class TaskView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(TaskView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'task.html')


@method_decorator(auth_admin, name='dispatch')
class ReadView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(ReadView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'read.html')