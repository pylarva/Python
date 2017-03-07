from django.shortcuts import render
from cmdb import models
import json
from django.shortcuts import HttpResponse
from django.shortcuts import redirect

# Create your views here.


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
        print(name, ip, business, status, idc_name, idc_cabinet, person, ctime)

        models.HostDatabase.objects.create(name=name, ip=ip, business=business, status=status, idc_name=idc_name,
                                           idc_cabinet=idc_cabinet, person=person, ctime=ctime)

        data_dict['status'] = True
        data_dict['message'] = 'ok'
        return HttpResponse(json.dumps(data_dict))

    data_list = models.HostDatabase.objects.all()
    print(data_list)
    return render(request, 'hosts.html', {'data': data_list})


def users(request):
    return render(request, 'users.html')


def details(request):
    nid = request.GET.get('nid')
    print(request, nid)
    nid = int(nid)
    data_list = models.HostDatabase.objects.filter(id=nid)
    print(data_list[0].id)
    return render(request, 'details.html', {'data': data_list[0]})


def delete_host(request):
    nid = request.GET.get('nid')
    print(nid)
    models.HostDatabase.objects.filter(id=nid).delete()
    return redirect('/hosts/')



