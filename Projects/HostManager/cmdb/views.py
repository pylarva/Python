from django.shortcuts import render
from cmdb import models
import json
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from utils import pagination


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

    data_total = models.HostDatabase.objects.all().count()
    data_list = models.HostDatabase.objects.all()
    business_list = models.BusinessLine.objects.all()
    status_list = models.HostStatus.objects.all()
    print(data_total)

    # for p in range(109):
    #     p = str(p)
    #     models.HostDatabase.objects.create(name="salt"+p, ip="172.16.2."+p, business_id=1, status_id=1)

    # 分页切片显示主机数据
    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    page_obj = pagination.Page(current_page, data_total)
    data = data_list[page_obj.start:page_obj.end]
    page_str = page_obj.page_str('/hosts/')

    return render(request, 'hosts.html', {'data': data, 'business_list': business_list, 'status_list': status_list, 'page_str': page_str})


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

    if request.method == "POST":
        app_name = request.POST.get('app_name')
        host_list = request.POST.getlist('host_list')
        print(app_name, host_list)

        if not app_name or host_list == ['']:
            data_dict['status'] = False
            data_dict['message'] = '输入不能为空'
            return HttpResponse(json.dumps(data_dict))

        models.AppDatabase.objects.create(name=app_name)
        obj = models.AppDatabase.objects.get(name=app_name)
        obj.r.add(*host_list)

        data_dict['status'] = True
        data_dict['message'] = 'ok'
        return HttpResponse(json.dumps(data_dict))

    obj = models.AppDatabase.objects.all()  # app列表
    host_list = models.HostDatabase.objects.all()  # 主机列表
    data_total = models.AppDatabase.objects.all().count()
    print(obj)
    print(host_list[0].name)

    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    page_obj = pagination.Page(current_page, data_total)
    data = obj[page_obj.start:page_obj.end]
    page_str = page_obj.page_str('/app/')

    return render(request, 'app.html', {'obj_list': obj, 'host_list': host_list, 'data': data, 'page_str': page_str})


def delete_app(request, nid):

    if request.method == "POST":
        nid = int(nid)
        print(nid)
        models.AppDatabase.objects.filter(id=nid).delete()

        data_dict['status'] = True
        data_dict['message'] = 'ok'
        return HttpResponse(json.dumps(data_dict))


def details_app(request, nid):

    if request.method == "POST":
        nid = int(nid)
        obj = models.AppDatabase.objects.filter(id=nid).first()
        # print(obj.name)

        data_dict['name'] = obj.name
        data_dict['message'] = 'ok'
        return HttpResponse(json.dumps(data_dict))


def updata_app(request):

    if request.method == "POST":
        nid = request.POST.get('nid')
        name = request.POST.get('name')
        host_list = request.POST.getlist('host_list')
        print(nid, name, host_list)

        if not name or host_list == ['']:
            data_dict['status'] = False
            data_dict['message'] = '输入不能为空'
            return HttpResponse(json.dumps(data_dict))

        obj = models.AppDatabase.objects.filter(id=nid).first()
        obj.name = name
        obj.r.set(host_list)
        obj.save()

        data_dict['status'] = True
        data_dict['message'] = 'ok'
        return HttpResponse(json.dumps(data_dict))


u_list = []
for i in range(109):
    u_list.append(i)


def user_list(request):
    current_page = request.GET.get('p', 1)

    current_page = int(current_page)
    page_obj = pagination.Page(current_page, len(u_list))
    data = u_list[page_obj.start:page_obj.end]
    page_str = page_obj.page_str('/user_list/')

    return render(request, 'user_list.html', {'user_list': data, 'page_str': page_str})