#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from web.service import audit
from web.service import audit_db
from web.service.login import auth_db


@method_decorator(auth_db, name='dispatch')
class ApplyListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(ApplyListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'audit_db.html')


class ApplyJsonView(View):
    def get(self, request):
        obj = audit_db.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = audit_db.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = audit_db.Asset.put_assets(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = audit_db.Asset.post_assets(request)
        return JsonResponse(response.__dict__)


class ReleaseReadListView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(ReleaseReadListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'release_r.html')