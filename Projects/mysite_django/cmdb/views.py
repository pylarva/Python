from django.shortcuts import render
from cmdb import models
from django.shortcuts import redirect
from django.shortcuts import HttpResponse

# Create your views here.


def index(request):
    # return HttpResponse('123')
    if(request.method == "POST"):
        u = request.POST.get('username', None)
        e = request.POST.get('email', None)
        # 插入数据
        models.UserInfo.objects.create(user=u, email=e)
        # print(user, email)

    data_list = models.UserInfo.objects.all()
    # [UserInfo对象, UserInfo对象]...
    return render(request, 'index.html', {'data': data_list})
    # return redirect('/index/')
