#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import server
from web.service import ippool
from repository import models
from utils.response import BaseResponse
from web.service.login import auth_admin
from utils.menu import menu


@method_decorator(auth_admin, name='dispatch')
class ServerListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(ServerListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'server_install.html')

    def post(self, request, *args, **kwargs):
        # 前端新添加装机任务 检查是否允许装机 再添加装机任务
        response = BaseResponse()
        response.status = True
        ilo_ip = request.POST.get("ilo_ip")
        if ilo_ip:
            server_obj = models.DellServer.objects.filter(manage_ip=ilo_ip).first()
            if server_obj.manage_ip != 2:
                response.status = False
                response.message = '物理机已被安装系统或者为故障机'
            else:
                pass
        return JsonResponse(response.__dict__)


class ServerJsonView(View):
    def get(self, request):
        obj = server.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = server.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = server.Asset.put_assets(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = server.Asset.post_assets(request)
        return JsonResponse(response.__dict__)


