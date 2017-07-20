#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from django.db.models import Q
from django.views import View
from repository import models
from django.shortcuts import render
from django.http import JsonResponse
from utils.response import BaseResponse
from web.service import project


class ProjectsListView(View):
    def get(self, request, *args, **kwargs):
        data_list = models.ProjectTask.objects.all()
        return render(request, 'project_list.html', {'data_list': data_list})

    def post(self, request, *args, **kwargs):
        """
        project_list.html 页面循环发送ajax 查询发布任务状态 如果为发布中则进行前端展示
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = BaseResponse()
        task_id = request.POST.getlist('task_id')
        # task_id_list = ['310', '311']
        task_id_list = task_id
        con_q = Q()
        con_q.connector = 'OR'
        for item in task_id_list:
            con_q.children.append(('id', item))
        # print(con_q)
        obj_list = models.ReleaseTask.objects.filter(con_q).values('id', 'release_status')
        # print(obj_list)
        # <QuerySet [{'id': 310, 'release_status': 2}, {'id': 311, 'release_status': 2}]>

        # obj = models.ReleaseTask.objects.filter(id=task_id).first()
        # task_status = obj.release_status
        # print(task_status)
        response.status = True
        # response.data = {'status': task_status, 'data_list': list(obj_list)}
        response.data = {'data_list': list(obj_list)}
        return JsonResponse(response.__dict__)


class ProjectsJsonView(View):
    def get(self, request):
        obj = project.Project()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = project.Project.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = project.Project.put_assets(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        obj = project.Project()
        response = obj.post_task(request)
        return JsonResponse(response.__dict__)


class ProjectsReadListView(View):
    def get(self, request, *args, **kwargs):
        data_list = models.ProjectTask.objects.all()
        return render(request, 'project_list_r.html', {'data_list': data_list})

    def post(self, request, *args, **kwargs):
        """
        project_list.html 页面循环发送ajax 查询发布任务状态 如果为发布中则进行前端展示
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = BaseResponse()
        task_id = request.POST.get('task_id')
        obj = models.ReleaseTask.objects.filter(id=task_id).first()
        task_status = obj.release_status
        # print(task_status)
        response.status = True
        response.data = {'status': task_status}
        return JsonResponse(response.__dict__)



