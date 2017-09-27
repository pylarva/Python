#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import env
from repository import models
from utils.response import BaseResponse
from web.service.login import auth
from utils.menu import menu


@method_decorator(auth, name='dispatch')
class AssetListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(AssetListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        business_two_list = models.BusinessTwo.objects.all()
        return render(request, 'env_list.html', {'business_two_list': business_two_list})


class AssetJsonView(View):
    def get(self, request):
        obj = env.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = env.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = env.Asset.put_assets(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = env.Asset.post_assets(request)
        return JsonResponse(response.__dict__)


