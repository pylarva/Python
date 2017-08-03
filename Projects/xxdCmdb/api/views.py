#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import importlib
from django.views import View
from django.http import JsonResponse
from utils.response import BaseResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# from utils import auth
from api import config
from repository import models
from api.service import asset


class LimitView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(LimitView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = BaseResponse()

        name = kwargs.get('n1', None)
        if name:
            try:
                result = models.AuthInfo.objects.filter(username=name, status=2).values('username', 'ip', 'hostname', 'rank')
                response.data = list(result)
                response.status = True
                return JsonResponse(response.__dict__)
            except Exception as e:
                response.error = "Didn't find %s" % name
                response.status = False
                return JsonResponse(response.__dict__)

        result = models.AuthInfo.objects.all().values('username', 'ip', 'hostname', 'rank', 'status')
        # result = models.AuthInfo.objects.all()
        response.data = list(result)
        response.status = True
        return JsonResponse(response.__dict__)


class AssetView(View):
    # @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AssetView, self).dispatch(request, *args, **kwargs)

    # @method_decorator(auth.api_auth)
    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # appid = request.META.get(['HTTP_APPID'], None)
        # print(appid)
        # test = {'user': '用户名', 'pwd': '密码'}
        # result = json.dumps(test,ensure_ascii=True)
        # result = json.dumps(test,ensure_ascii=False)
        # return HttpResponse(result)

        # test = {'user': '用户名', 'pwd': '密码'}
        # result = json.dumps(test,ensure_ascii=True)
        # result = json.dumps(test,ensure_ascii=False)
        # return HttpResponse(result,content_type='application/json')

        # test = {'user': '用户名', 'pwd': '密码'}
        # return JsonResponse(test, json_dumps_params={"ensure_ascii": False})
        from django.db.models import Q

        # response = asset.get_untreated_servers()
        response = BaseResponse()

        # print(kwargs)
        b1 = kwargs.get('b1', None)
        b2 = kwargs.get('b2', None)
        b3 = kwargs.get('b3', None)
        if b1:
            try:
                b1_id = models.BusinessOne.objects.filter(name=kwargs['b1']).first().id
                if b2:
                    try:
                        b2_id = models.BusinessTwo.objects.filter(name=kwargs['b2']).first().id
                        if b3:
                            try:
                                b3_id = models.BusinessThree.objects.filter(name=kwargs['b3']).first().id

                                condition = Q()
                                con_business_1 = Q()
                                con_business_1.children.append(('business_1', b1_id))
                                con_business_2 = Q()
                                con_business_2.children.append(('business_2', b2_id))
                                con_business_3 = Q()
                                con_business_3.children.append(('business_3', b3_id))

                                condition.add(con_business_1, 'AND')
                                condition.add(con_business_2, 'AND')
                                condition.add(con_business_3, 'AND')

                                result = models.Asset.objects.filter(condition).values('host_ip', 'host_name', 'business_2__name')
                                response.data = list(result)
                                response.status = True
                                return JsonResponse(response.__dict__)
                            except Exception as e:
                                response.error = "Didn't find %s" % kwargs['b3']
                                response.status = False
                                return JsonResponse(response.__dict__)
                        print(b2_id)
                        condition = Q()
                        con_business_1 = Q()
                        con_business_1.children.append(('business_1', b1_id))
                        con_business_2 = Q()
                        con_business_2.children.append(('business_2', b2_id))

                        condition.add(con_business_1, 'AND')
                        condition.add(con_business_2, 'AND')

                        result = models.Asset.objects.filter(condition).values('host_ip', 'host_name', 'business_2__name')
                        response.data = list(result)
                        response.status = True
                        return JsonResponse(response.__dict__)
                    except Exception as e:
                        response.error = "Didn't find %s" % kwargs['b2']
                        response.status = False
                        return JsonResponse(response.__dict__)

                print(b1_id)
                condition = Q()
                con_business_1 = Q()
                con_business_1.children.append(('business_1', b1_id))

                condition.add(con_business_1, 'AND')

                result = models.Asset.objects.filter(condition).values('host_ip')
                response.data = list(result)
                response.status = True
                return JsonResponse(response.__dict__)

            except Exception as e:
                response.error = "Didn't find %s" % kwargs['b1']
                response.status = False
                return JsonResponse(response.__dict__)
        result = models.Asset.objects.all().values('host_ip')
        response.data = list(result)
        response.status = True

        return JsonResponse(response.__dict__)

    # @method_decorator(auth.api_auth)
    def post(self, request, *args, **kwargs):
        """
        更新或者添加资产信息
        :param request:
        :param args:
        :param kwargs:
        :return: 1000 成功;1001 接口授权失败;1002 数据库中资产不存在
        """

        server_info = json.loads(request.body.decode('utf-8'))
        server_info = json.loads(server_info)
        hostname = server_info['k1']
        #
        ret = {'code': 1000, 'message': '[%s]更新完成' % hostname}
        #
        # server_obj = models.Server.objects.filter(hostname=hostname).select_related('asset').first()
        # if not server_obj:
        #     ret['code'] = 1002
        #     ret['message'] = '[%s]资产不存在' % hostname
        #     return JsonResponse(ret)
        #
        # for k, v in config.PLUGINS_DICT.items():
        #     module_path, cls_name = v.rsplit('.', 1)
        #     cls = getattr(importlib.import_module(module_path), cls_name)
        #     response = cls.process(server_obj, server_info, None)
        #     if not response.status:
        #         ret['code'] = 1003
        #         ret['message'] = "[%s]资产更新异常" % hostname
        #     if hasattr(cls, 'update_last_time'):
        #         cls.update_last_time(server_obj, None)

        return JsonResponse(ret)


class ReleaseView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(ReleaseView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = BaseResponse()

        name = kwargs.get('n1', None)
        if name:
            try:
                result = models.AuthInfo.objects.filter(username=name, status=2).values('username', 'ip', 'hostname', 'rank')
                response.data = list(result)
                response.status = True
                return JsonResponse(response.__dict__)
            except Exception as e:
                response.error = "Didn't find %s" % name
                response.status = False
                return JsonResponse(response.__dict__)

        result = models.ReleaseTask.objects.all().values('username', 'ip', 'hostname', 'rank', 'status')
        # result = models.AuthInfo.objects.all()
        response.data = list(result)
        response.status = True
        return JsonResponse(response.__dict__)

    def post(self, request, *args, **kwargs):
        response = BaseResponse()

        n1 = json.loads(request.body.decode('utf-8'))
        n1 = json.loads(n1)

        r_id = n1.get('id', None)
        msg = n1.get('msg', None)

        # 上传包md5值
        md5 = n1.get('md5', None)
        if md5:
            print(md5)
            models.ReleaseTask.objects.filter(id=r_id).update(release_md5=md5)
            models.ReleaseLog.objects.create(release_id=r_id, release_msg=md5)
            # 发布任务成功上传
            response.status = True
            return JsonResponse(response.__dict__)

        print(r_id, msg)
        try:
            models.ReleaseLog.objects.create(release_id=r_id, release_msg=msg)
            response.status = True
        except Exception as e:
            response.status = False

        obj = models.ReleaseLog.objects.filter(release_time__gt='2017-05-19 05:00').first()
        print(obj.release_time)

        return JsonResponse(response.__dict__)