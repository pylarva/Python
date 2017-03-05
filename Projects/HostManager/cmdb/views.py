from django.shortcuts import render
from cmdb import models
import json
from django.shortcuts import HttpResponse

# Create your views here.


def login(request):

    data_dict = {'status': False, 'message': ""}

    if request.method == "POST":
        print(request.POST)
        u1 = request.POST.get('username1', None)
        p1 = request.POST.get('pwd1', None)

        if u1 == '1' and p1:
            print(u1, p1)
            user_num = models.UserInfo.objects.filter(username=u1, pwd=p1).count()
            # if user_num < 1:
            #     pass
            data_dict['status'] = True
            data_dict['message'] = 'ok'
            return HttpResponse(json.dumps(data_dict))
        elif u1 == '2' and p1:
            print(u1, p1)
            data_dict['message'] = 'no'
            return HttpResponse(json.dumps(data_dict))

        u2 = request.POST.get('username2', None)
        p2 = request.POST.get('pwd2', None)
        qq = request.POST.get('qq', None)

        if u2 and p2:
            print(u2, p2, qq)
            data_dict['status'] = True
            data_dict['message'] = 'ok...'
            result = data_dict
            return HttpResponse(json.dumps(result))

        print(u1, p1, u2, p2, qq)
    return render(request, 'login.html')


