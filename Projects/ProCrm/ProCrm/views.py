from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate


def acc_login(request):
    """
    用户登陆
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            print(user)
            login(request, user)
            return redirect("/crm")
    return render(request, "login.html")


def acc_logout(request):
    """
    用户注销
    :param request:
    :return:
    """
    logout(request)
    return redirect("login.html")