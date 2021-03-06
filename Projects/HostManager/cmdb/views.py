from django.shortcuts import render
from cmdb import models
import json
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from util import pagination


# Create your views here.

data_dict = {'status': False, 'message': ""}

USER_NAME = {}


def auth(func):
    def inner(request, *args, **kwargs):
        # v = request.COOKIES.get('user_cookie')
        v = request.session.get('is_login', None)
        print(v)
        if not v:
            return redirect('/login/')
        global USER_NAME
        USER_NAME['name'] = v
        return func(request, *args, **kwargs)
    return inner


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
                # res = HttpResponse(json.dumps(data_dict))
                # res.set_cookie('user_cookie', u1)

                # 设置session
                request.session['username'] = u1
                request.session['is_login'] = True

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


def logout(request):
    # 注销
    request.session.clear()
    return redirect('/login/')


@auth
def home(request):

    # 如果用户点击了注销 会往/home/ 发ajax请求 直接设置cookie超时时间为0 注销
    if request.method == 'POST':
        cookie_name = request.COOKIES.get('username')
        data_dict['status'] = True
        data_dict['message'] = 'ok'
        res = HttpResponse(json.dumps(data_dict))
        res.set_cookie('user_cookie', cookie_name, max_age=0)
        return res

    if request.method == 'GET':
        pass

    return render(request, 'home.html')


@auth
def hosts(request):

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

    # 获取用户通过cookie传过来的自定义显示数
    val = request.COOKIES.get('per_page_count', 10)
    page_init = {}
    page_init['per_page_count'] = val
    print(val)
    val = int(val)

    page_obj = pagination.Page(current_page, data_total, val)
    data = data_list[page_obj.start:page_obj.end]
    page_str = page_obj.page_str('/hosts/')

    return render(request, 'hosts.html', {'data': data, 'business_list': business_list, 'status_list': status_list,
                                          'page_str': page_str, 'user_name': USER_NAME, 'page_init': page_init})


@auth
def users(request):
    return render(request, 'users.html')


@auth
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


@auth
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

    return render(request, 'app.html', {'obj_list': obj, 'host_list': host_list, 'data': data,
                                        'page_str': page_str, 'user_name': USER_NAME})


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

from django import forms
from django.forms import widgets
from django.forms import fields


class FM(forms.Form):
    user = fields.CharField(
        error_messages={'required': '用户名不能为空'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
        label='用户名',
    )

    pwd = fields.CharField(
        min_length=6,
        error_messages={'required': '密码不能为空', 'min_length': '密码长度不能小于6'},
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}),
        label='密码',
    )

    email = fields.EmailField(
        error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'},
        widget=widgets.EmailInput(attrs={'class': 'form-control', 'type': 'email'})
    )

    city1 = fields.ChoiceField(
        # widget=widgets.ChoiceInput(attrs={'class': 'selectpicker'}),
        choices=[(0, '上海'), (1, '北京'), (2, '广州')], label='城市',

    )


def fm(request):
    if request.method == 'GET':
        obj = FM()
        return render(request, 'users.html', {'obj': obj})

    elif request.method == 'POST':
        obj = FM(request.POST)
        ret = obj.is_valid()
        if ret:
            u = request.POST.get('user')
            p = request.POST.get('pwd')
            user_obj = models.UserInfo(username=u, pwd=p)
            user_obj.save()
            return redirect('/users/')
        else:
            return render(request, 'users.html', {'obj': obj})
