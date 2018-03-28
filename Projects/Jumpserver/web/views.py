import os
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here


@login_required()
def dashboard(request):
    return render(request, 'index.html')


def racc_login(request):
    err_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            err_msg = 'Wrong username or password...'
    return render(request, 'signin.html', {'err_msg': err_msg})


def acc_logout(request):
    logout(request)
    return redirect("/login")


@login_required()
def user_auth(request):
    dir_list = os.listdir(settings.AUDIT_LOG_DIR)
    return render(request, 'user_auth.html', {'dir_list': dir_list})


def audit_log_date(request, log_date):
    pass