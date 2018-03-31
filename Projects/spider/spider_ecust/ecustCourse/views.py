import json
import requests
from conf import config
from contextlib import closing
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
    r3 = requests.get(url='%s/student/allcourse.aspx' % config.school_url, cookies=cookies_dict)

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

        cookies_dict_obj = models.UserProfile.objects.filter(username=username).first()
        password = cookies_dict_obj.pwd
        cookies_dict = eval(cookies_dict_obj.user_cookies)

        course_url = '%s/student/%s' % (config.school_url, course_id)
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0",
                   "Connection": "close", "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Upgrade-Insecure-Requests": "1",
                   'Referer': 'http://222.73.34.165:88/student/allcourse.aspx'}
        print(course_url)

        # r1 = requests.get(url=config.script_1)
        # r2 = requests.get(url=config.script_2)

        r3 = requests.get(url=course_url,
                          cookies=cookies_dict)
        print(r3.headers['Content-Length'])
        print(r3.text)

        # r = requests.get(course_url, stream=True)
        # if int(r.headers['content-length']) < 68221:
        #     content = r.content
        #     print(content)

        # with closing(requests.get(url=course_url, headers=headers, cookies=cookies_dict, stream=True)) as r:
        #     for line in r.iter_lines():
        #         if line:
        #             print(line)
        # with open('11111', 'wb') as fd:
        #     for chunk in r.iter_content(100):
        #         fd.write(chunk)

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
        soup = BeautifulSoup(r1.text, 'html.parser')
        s1 = soup.find(id="__VIEWSTATE").get('value')
        s2 = soup.find(id="__VIEWSTATEGENERATOR").get('value')

        r1_cookies_dict = r1.cookies.get_dict()

        new_url = '%s/login.aspx' % config.school_url
        response = requests.post(url=new_url,
                                 data={'__VIEWSTATE': s1,
                                       '__VIEWSTATEGENERATOR': s2,
                                       '__EVENTTARGET': '',
                                       '__EVENTARGUMENT': '',
                                       'Button1': '确认登陆',
                                       'username': username,
                                       'pwd': password,
                                       'gtpath': ''},
                                 cookies=r1_cookies_dict)

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
