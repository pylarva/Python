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
from web.service import project_r
from web.service import project_read
from django.utils.decorators import method_decorator
from web.service.login import auth_admin


# @method_decorator(auth_admin, name='dispatch')
class ProjectsListView(View):
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

        break_id = request.POST.get('break_id', None)
        # 中断发布任务
        if break_id:
            models.ReleaseTask.objects.filter(id=break_id).update(release_status=3)
            response.status = True
            return JsonResponse(response.__dict__)

        roll_back_id = request.POST.get('roll_back', None)
        # 回滚任务ID
        if roll_back_id:
            release_env = request.POST.get('release_env', None)
            release_env_obj = models.BusinessOne.objects.filter(id=release_env).first()
            release_env_name = release_env_obj.name
            obj = models.ProjectTask.objects.filter(id=roll_back_id).first()
            business_2_id = obj.business_2_id
            # 查询最近一次提交的分支名
            try:
                release_obj = models.ReleaseTask.objects.filter(release_name_id=business_2_id, release_status='2',
                                                                release_env_id=release_env).last()
                success_branch = release_obj.release_git_branch
                success_time = release_obj.release_time
                response.data = {'branch': success_branch, 'time': success_time, 'env': release_env_name}
                response.status = True
            except Exception as e:
                print(e)
                response.status = False
            return JsonResponse(response.__dict__)

        # 前端页面请求任务状态
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


class ProjectsJsonReadView(View):
    """
    开发用户读取的项目列表页面 支持发布申请
    """
    def get(self, request):
        obj = project_r.ProjectRead()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        obj = project_r.ProjectRead()
        response = obj.post_task(request)
        return JsonResponse(response.__dict__)


class ProjectListView(View):
    def get(self, request, *args, **kwargs):
        data_list = models.ProjectTask.objects.all()
        return render(request, 'project_read.html', {'data_list': data_list})


class ProjectJsonReadView(View):
    """
    普通用户读取的项目列表页面
    """

    def get(self, request):
        obj = project_read.ProjectRead()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        obj = project_r.ProjectRead()
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



