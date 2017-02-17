from django.shortcuts import render
from django.shortcuts import HttpResponse
from demo_jd import models

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
    return render(request, 'login.html',)


def register(request):

    if(request.method == "POST"):
        u = request.POST.get('user_name', None)
        p = request.POST.get('user_pwd', None)
        h = request.POST.get('user_phone', None)
        e = request.POST.get('user_email', None)

        models.UserDatabase.objects.create(user=u, pwd=p, phone=h, email=e)

    data_list = models.UserDatabase.objects.all()
    print(data_list)
    return render(request, 'register.html', {'data': data_list})
