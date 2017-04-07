#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import paramiko
from repository import models
from io import StringIO
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse

from web.service import asset

data_dict = {'status': False, 'message': ""}


class VirtualListView(View):
    def get(self, request, *args, **kwargs):
        data = models.VirtualMachines.objects.all()
        host = models.HostMachines.objects.all()
        print(data)
        return render(request, 'virtual_list.html', {'data': data, 'host_list': host})

    def post(self, request, *args, **kwargs):
        v = request.POST.get('host_machine')
        new_name = request.POST.get('new_host_name')
        new_ip = request.POST.get('new_host_ip')
        machine_type = request.POST.get('machine_type')
        print(v, new_ip, new_name, machine_type)

        key_str = """-----BEGIN RSA PRIVATE KEY-----
        MIIEpAIBAAKCAQEAx8BCwoZYq/fwQ9Q1qXi/u52eEzmLNiDA/OZdaJhvduRPd7Xh
        drrkIm7IRpWawzoiVr5esTLA9n98on5vDE5QbP3VTWxAtnMXT3i6g2zenjRcH7pj
        8LxiZcxy8OyeMdoQcnKCKTeSi3MzX7p9r4qE9krYRMU5CoPV4vNuodb21kLtDXok
        5GiEQTxR1mCaxAYKlw7GM3bCNq9nKVOkwbnDx6tiHqWWOi2RbFGp6RQiNIRwv9px
        YCV3hjRhhsBHmjX7TzzMud4UK+TelMFDWW9W0/HReBZYhdiMOcWOnUBRuuzq26xm
        jm4ek2Z/YlYLpudtM0E7MbSXDc4Uay6Vjv+ClwIDAQABAoIBAQCVtE0UdxWrxMWI
        QFn7amjgFq/rHpxr875Pi+MDygL36wJ36JNSpZznBXoKFIOJv18O/dwAF9awpzlk
        mzdk1KjIFrEvNmuFkdotkIDQkN6DWSCWEt5mBPoF62VVlTC2kgTzkUhl1aV559vf
        6efakQk3gT52xA0NCWNalTEcD/ys9OavCw3TFyioLXgs3IJji4LOgu20sCu/mfBM
        wG4TnU+OElhXDQnQy/kvg2RSFGzBlGlaTfRljMGncf8LE0Sf1U2nQUmtbFWZcAR0
        9s6F1eiN1sTHlGyMikdBAxe+Xmr9eYxScs7whorWjYGYoTolo9sVW2z6kmqF2fN+
        +BddtFKBAoGBAOWpsDoe08uplzpWJRRetrhhH8VXlNMAZXzTZ5Ch+Qtp+1ef5VDK
        9Ifn4IMLdBmHHFCSFvbidSWNbH6jjHODqid2K0aTx6imvIndUZk/rMDcPQYiY4Vd
        k5/nPiouc7MB9DWD15P7Z807C4chMrdMCIWw4EzTtTNpUVhVYilqP/9XAoGBAN6o
        cB0+ls1O+QJT7olccdazY48mVQDwfZvkCQL15ehAkt32Gtt1dR8pEmR65QrPH2Gs
        v4zXBxGDbaBy/vWEgU1Hyx689JKnQw8QGM7znw74xI63hGKFHhQuvb1VDmDl2Cuu
        vdMysXK4+sqF9BwLcxbkELn3HXD+kIXlXCSP+M7BAoGAfjqvHrLU7ErRUQIKLVEF
        kv/nC3tg1DySi3JSqP8tuCVPPVEoJCj5ED3Ve5FvBZzqZip1rsq3YqWBrXVM/Cyw
        +DGOBaOyCLNkS042zElgNTyX2ehK1QGi4y+hTmPrucboKAXIFpEG85lxc5s+mdqT
        kI+wKOnv3UsUp71+T48Tj88CgYAMVulftYhF+Ip0RpKBqk3kyCxMUqODWdCcQxb8
        wwPqyylYg7sZTnkfMPeD+guXfcMPdrNm6sPJhK8epUDb+mvwDHqFSZOETSC6RPoa
        /gVinwbFogYEL7xrAewiAgS5+gLw6M48ViLfaMD9WE8e/sNyEVGb/MX07Sa1RPDG
        VfREAQKBgQDZ91mTadB09U5HXYNq0r2roxqdLRMWc0tFiCOJnelMJ7Ix+mQUh3sE
        T6DHO/D5779SW8xy8Fo0O3bHr41boCBgRn7/x4sxYiOPaR05Z9e4xW4GQvbSHs3F
        M3ccnsavjnp8EhqL/P+OP9YwqVmk+TH4nx4bQZegTn2DmIH8SRXCcQ==
        -----END RSA PRIVATE KEY-----"""

        try:
            private_key = paramiko.RSAKey(file_obj=StringIO(key_str))
            transport = paramiko.Transport((v, 22))
            transport.connect(username='root', pkey=private_key)
            ssh = paramiko.SSHClient()
            ssh._transport = transport

            models.VirtualMachines.objects.create(mudroom_host=v, host_name=new_name, host_ip=new_ip, item=machine_type)

            data_dict['status'] = True
            data_dict['message'] = "ok"
            return HttpResponse(json.dumps(data_dict))


        except Exception:

            data_dict['status'] = False
            data_dict['message'] = "no"
            return HttpResponse(json.dumps(data_dict))


class AssetJsonView(View):
    def get(self, request):
        obj = asset.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = asset.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = asset.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, device_type_id, asset_nid):
        response = asset.Asset.assets_detail(device_type_id, asset_nid)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class AddAssetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_asset.html')