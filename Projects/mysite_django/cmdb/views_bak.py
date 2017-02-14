from django.shortcuts import render
from django.shortcuts import HttpResponse

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
