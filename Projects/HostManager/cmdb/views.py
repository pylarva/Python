from django.shortcuts import render
from cmdb import models
import json
from django.shortcuts import HttpResponse

# Create your views here.


def login(request):

    data_dict = {'status': False, 'message': ""}

    if request.method == "POST":
        u1 = request.POST.get('username1', None)
        p1 = request.POST.get('pwd1', None)

        if u1 and p1:
            print(u1, p1)
            user_num = models.UserInfo.objects.filter(username=u1, pwd=p1).count()
            # if user_num < 1:
            #     pass
            data_dict['status'] = True
            data_dict['message'] = 'ok'
            return HttpResponse(json.dumps(data_dict))
    return render(request, 'login.html')


