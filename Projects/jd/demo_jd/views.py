from django.shortcuts import render
from django.shortcuts import HttpResponse
from demo_jd import models
from django.shortcuts import redirect

# Create your views here.

USER_INPUT = [
    {'user': 'u1', 'email': 'e1'},
    {'user': 'u2', 'email': 'e2'},
]


# 处理用户请求
def index(request):
    # return HttpResponse('123')
    if(request.method == "POST"):
        user = request.POST.get('username', None)
        email = request.POST.get('email', None)
        temp = {'user': user, 'email': email}
        USER_INPUT.append(temp)
        print(user, email)

    # 模板引擎
    # 获取index.html + {'data': USER_INPUT}
    return render(request, 'index.html', {'data': USER_INPUT})


def login(request):

    if(request.method == "POST"):
        u = request.POST.get('user_name', None)
        p = request.POST.get('user_pwd', None)

        num = models.UserDatabase.objects.filter(user=u, pwd=p).count()

        if num > 0:
            return redirect('/index/')
        else:
            return HttpResponse('<meta http-equiv="refresh" content="5;url=http://127.0.0.1:8001/login/">'
                                '[ %s ]登陆失败, 用户名或者密码错误...' % u)

    return render(request, 'login.html',)


def register(request):

    if(request.method == "POST"):
        u = request.POST.get('user_name', None)
        p = request.POST.get('user_pwd', None)
        h = request.POST.get('user_phone', None)
        e = request.POST.get('user_email', None)

        num = models.UserDatabase.objects.filter(user=u).count()

        if num > 0:
            return HttpResponse('注册失败,[%s]该用户名已被注册...' % u)
        else:
            models.UserDatabase.objects.create(user=u, pwd=p, phone=h, email=e)
            return HttpResponse('<meta http-equiv="refresh" content="5;url=http://127.0.0.1:8001/login/">'
                                '注册成功! 5秒后跳转登陆...')

    data_list = models.UserDatabase.objects.all()
    # for item in data_list:
    #     print(item)
    # print(data_list)
    return render(request, 'register.html', {'data': data_list})
