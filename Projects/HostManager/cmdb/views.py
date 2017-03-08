from django.shortcuts import render
from cmdb import models
import json
from django.shortcuts import HttpResponse
from django.shortcuts import redirect

# Create your views here.

data_dict = {'status': False, 'message': ""}


def login(request):

    data_dict = {'status': False, 'message': ""}

    if request.method == "POST":
        print(request.POST)
        u1 = request.POST.get('username1', None)
        p1 = request.POST.get('pwd1', None)

        if u1 or p1:

            user_num = models.UserInfo.objects.filter(username=u1, pwd=p1).count()

            if user_num > 0:
                print(u1, p1, user_num)
                data_dict['status'] = True
                data_dict['message'] = 'ok'
                return HttpResponse(json.dumps(data_dict))
            else:
                data_dict['message'] = '用户名或者密码错误...'
                return HttpResponse(json.dumps(data_dict))

        u2 = request.POST.get('username2', None)
        p2 = request.POST.get('pwd2', None)
        qq = request.POST.get('qq', None)

        if u2 and p2:
            # print(u2, p2, qq)
            data_dict['status'] = True
            data_dict['message'] = 'ok...'
            result = data_dict
            return HttpResponse(json.dumps(result))

        # print(u1, p1, u2, p2, qq)
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def hosts(request):
    data_dict = {'status': False, 'message': ""}

    if request.method == 'POST':
        name = request.POST.get('name')
        ip = request.POST.get('ip')
        business = request.POST.get('business')
        status = request.POST.get('status')
        idc_name = request.POST.get('idc_name')
        idc_cabinet = request.POST.get('idc_cabinet')
        person = request.POST.get('person')
        ctime = request.POST.get('ctime')

        if not name or not ip:
            data_dict['status'] = False
            data_dict['message'] = "输入不能为空"
            return HttpResponse(json.dumps(data_dict))
        else:
            print(name, ip, business, status, idc_name, idc_cabinet, person, ctime)
            models.HostDatabase.objects.create(name=name, ip=ip, business_id=business, status_id=status, idc_name=idc_name,
                                               idc_cabinet=idc_cabinet, person=person, ctime=ctime)
            data_dict['status'] = True
            data_dict['message'] = 'ok'
            return HttpResponse(json.dumps(data_dict))

    data_list = models.HostDatabase.objects.all()
    business_list = models.BusinessLine.objects.all()
    status_list = models.HostStatus.objects.all()
    print(data_list)
    return render(request, 'hosts.html', {'data': data_list, 'business_list': business_list, 'status_list': status_list})


def users(request):
    return render(request, 'users.html')


def details(request, nid):

    data_dict = {}

    if request.method == "POST":
        nid = int(nid)
        data_list = models.HostDatabase.objects.filter(id=nid).first()
        data_dict['id'] = data_list.id
        data_dict['name'] = data_list.name
        data_dict['ip'] = data_list.ip
        data_dict['business_id'] = data_list.business_id
        data_dict['idc_name'] = data_list.idc_name
        data_dict['idc_cabinet'] = data_list.idc_cabinet
        data_dict['person'] = data_list.person
        # data_dict['ctime'] = data_list.ctime
        data_dict['status_id'] = data_list.status_id
        print(data_list.name)
        return HttpResponse(json.dumps(data_dict))

    print(request, nid)
    nid = int(nid)
    data_list = models.HostDatabase.objects.filter(id=nid).first()
    print(data_list.name)
    return render(request, 'details.html', {'data': data_list})


def delete_host(request, nid):

    if request.method == "POST":
        nid = int(nid)
        print(nid)
        # 删除主机为nid数据
        models.HostDatabase.objects.filter(id=nid).delete()

        data_dict['status'] = True
        data_dict['message'] = 'ok'
        return HttpResponse(json.dumps(data_dict))


def updata(request):

    if request.method == 'POST':
        nid = request.POST.get('nid')
        name = request.POST.get('name')
        ip = request.POST.get('ip')
        business_id = request.POST.get('business')
        status_id = request.POST.get('status')
        idc_name = request.POST.get('idc_name')
        idc_cabinet = request.POST.get('idc_cabinet')
        person = request.POST.get('person')
        print(nid, name, ip, business_id, status_id, idc_name, idc_cabinet, person)

        models.HostDatabase.objects.filter(id=nid).update(name=name, ip=ip, business_id=business_id,
                                                          status_id=status_id, idc_name=idc_name,
                                                          idc_cabinet=idc_cabinet, person=person)

        data_dict['status'] = True
        data_dict['message'] = 'ok'
        return HttpResponse(json.dumps(data_dict))


def app(request):
    obj = models.AppDatabase.objects.all()  # app列表
    host_list = models.HostDatabase.objects.all()  # 主机列表
    print(obj)
    print(host_list[0].name)
    return render(request, 'app.html', {'obj_list': obj, 'host_list': host_list})