import requests
from conf import config
from bs4 import BeautifulSoup
from ecustCourse import models
from django.shortcuts import render, redirect


def all_course(request, username, password, cookies_dict):
    """
    爬取所有课程
    :param request:
    :param username:
    :param password:
    :param cookies_dict:
    :return:
    """
    s1 = '/wEPDwULLTEwMTQ2MjE4MjhkZC0kr8EqVmReGz8wShIStvlReqepxl2ifQoJhTN8zjbL'
    s2 = 'C2EE9ABB'

    r3 = requests.post(url='%s/student/allcourse.aspx' % config.school_url,
                       data={'__VIEWSTATE': s1,
                             '__VIEWSTATEGENERATOR': s2,
                             '__EVENTTARGET': '',
                             '__EVENTARGUMENT': '',
                             'Button1': '确认登陆',
                             'username': username,
                             'pwd': password,
                             'gtpath': ''},
                       cookies=cookies_dict)

    soup = BeautifulSoup(r3.text, 'html.parser')

    td_list = soup.find(id='learnedlist').find_all(name='td')

    data = []
    for i in td_list:
        course_dict = {}
        title = i.find(name='span')
        if not title:
            continue
        course_dict['title'] = title.text
        course_dict['url'] = i.find(name='a').get('href')
        course_dict['img'] = '%s%s' % (config.school_url, i.find(name='img').get('src').split('..')[1])
        data.append(course_dict)

    return data


def dashboard(request):
    if request.method == 'GET':
        username = request.session['username']
        cookies_dict_obj = models.UserProfile.objects.filter(username=username).first()
        password = cookies_dict_obj.pwd
        cookies_dict = eval(cookies_dict_obj.user_cookies)

        data = all_course(request, username, password, cookies_dict)

        return render(request, 'index.html', {'data': data})

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        username = request.session['username']

        print(course_id)
        s1 = '/wEPDwULLTEwMTQ2MjE4MjhkZC0kr8EqVmReGz8wShIStvlReqepxl2ifQoJhTN8zjbL'
        s2 = 'C2EE9ABB'

        cookies_dict_obj = models.UserProfile.objects.filter(username=username).first()
        password = cookies_dict_obj.pwd
        cookies_dict = eval(cookies_dict_obj.user_cookies)

        course_url = '%s/student/%s' % (config.school_url, course_id)
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0",
                   "Connection": "close", "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Upgrade-Insecure-Requests": "1"}
        print(course_url)

        r3 = requests.get(url=course_url,
                          headers=headers,
                          allow_redirects=False,
                          cookies=cookies_dict)
        print(r3.text)
        soup = BeautifulSoup(r3.text, 'html.parser')

    return render(request, 'index.html')


def acc_login(request):
    err_msg = ''
    if request.method == 'POST':
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        username = '26160554'
        password = 'Bingo_1991'

        # 尝试登陆学校网站
        cookies_dict = {}
        r1 = requests.get(url=config.school_url)
        r1_cookies_dict = r1.cookies.get_dict()

        s1 = '/wEPDwULLTEwMTQ2MjE4MjhkZC0kr8EqVmReGz8wShIStvlReqepxl2ifQoJhTN8zjbL'
        s2 = 'C2EE9ABB'
        # c1 = {'JSESSIONID': 'B72DDBA8B6E199D9006D9F4C72B675B4', 'ASP.NET_SessionId': 'no0qatloubof1dmj0jzjbycr'}

        response = requests.post(url='%s/login.aspx' % config.school_url,
                                 data={'__VIEWSTATE': s1,
                                       '__VIEWSTATEGENERATOR': s2,
                                       '__EVENTTARGET': '',
                                       '__EVENTARGUMENT': '',
                                       'Button1': '确认登陆',
                                       'username': username,
                                       'pwd': password,
                                       'gtpath': ''},
                                 cookies=r1_cookies_dict)
        # print(response.text)
        r2_cookies_dict = response.cookies.get_dict()
        if not r2_cookies_dict:
            err_msg = '用户名或密码错误..'
            return render(request, 'login.html', {'err_msg': err_msg})

        # 登陆成功记录用户名和cookies
        cookies_dict.update(r1_cookies_dict)
        cookies_dict.update(r2_cookies_dict)
        try:
            models.UserProfile.objects.create(username=username, pwd=password, user_cookies=cookies_dict)
        except Exception as e:
            print('%s user is exist...' % username)

        models.UserProfile.objects.filter(username=username).update(user_cookies=cookies_dict)

        request.session['username'] = username
        request.session['is_login'] = True
        data = all_course(request, username, password, cookies_dict)
        return render(request, 'index.html', {'data': data})

    return render(request, 'login.html', {'err_msg': err_msg})
