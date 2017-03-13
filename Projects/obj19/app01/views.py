from django.shortcuts import render
from django.shortcuts import redirect, HttpResponse
from django.shortcuts import HttpResponse

# Create your views here.


def index(request):
    # 获取当前用户的随机字符串 根据该字符串查找对应信息
    if request.session.get('is_login', None):
        return render(request, 'index.html', {'username': request.session['username']})
    else:
        return HttpResponse('no')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('pwd')
        print(u, p)
        if u == "root" and p == '123':

            # 设置session
            request.session['username'] = u
            request.session['is_login'] = True

            return redirect('/index/')
        else:
            return render(request, 'login.html')
    # return render(request, 'login.html')


def logout(request):
    request.session.clear()
    return redirect('/login/')
