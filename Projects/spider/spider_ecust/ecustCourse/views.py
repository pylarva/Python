import json
import re
import requests
import time
import threading
from conf import config
from contextlib import closing
from bs4 import BeautifulSoup
from django.http import JsonResponse
from ecustCourse import models
from utils.response import BaseResponse
from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor
from utils import logs
import requests


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
        course_dict['url'] = str(i.find(name='a').get('href')).split('=')[-1]
        course_dict['img'] = '%s%s' % (config.school_url, i.find(name='img').get('src').split('..')[1])
        data.append(course_dict)

    return data


def func(url, cookies_dict, headers, user):
    print(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
               "Connection": "keep-alive",
               "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               # "Content-Length": '696',
               'Cache-Control': 'max-age=0',
               "Content-Type": "application/x-www-form-urlencoded",
               "Upgrade-Insecure-Requests": "1",
               'Origin': 'http://222.73.34.165:88',
               'Referer': url,
               'Host': '222.73.34.165:88'}

    headers1 = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0",
                "Connection": "close",
                "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Upgrade-Insecure-Requests": "1",
                'Referer': 'http://222.73.34.165:88/student/allcourse.aspx'}

    r1 = requests.get(url=url,
                      headers=headers,
                      cookies=cookies_dict
                      )
    soup = BeautifulSoup(r1.text, 'html.parser')
    s1 = soup.find(id="__VIEWSTATE").get('value')
    s2 = soup.find(id="__VIEWSTATEGENERATOR").get('value')
    s3 = soup.find(id="hchapterid").get('value')
    s4 = soup.find(id="huserid").get('value')

    print(cookies_dict)
    print(s1, s2, s3, s4)

    i = 0
    while i < 28:
        time.sleep(5)
        r2 = requests.post(url=url,
                           headers=headers,
                           data={'__VIEWSTATE': s1,
                                 '__VIEWSTATEGENERATOR': s2,
                                 'Button2': '结束学习',
                                 'hchapterid': s3,
                                 'huserid': s4,
                                 'hlearntime': 3000},
                           cookies=cookies_dict)
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        times = 1
        try:
            msg = soup2.find(name='script').text
            times = int(re.search('\d+', msg).group())
            logs.logging.info('[%s] %s ...' % (user, msg))
        except Exception as e:
            pass
        if times > 45:
            break
        else:
            i += 1
    logs.logging.info('[%s] %s done...' % (user, url))

    return True


def course_details(request):
    if request.method == 'POST':
        response = BaseResponse()
        cookies_dict = request.session['cookies_dict']
        headers = request.session['headers']
        list_v = request.POST.getlist('list_v')
        user = request.session['user']

        # url = "http://222.73.34.165:88/student/schapter.aspx?chapterid=5771&add=1"
        # t = threading.Thread(target=func, args=(url, cookies_dict, headers, user))
        # t.start()

        url_list = []
        for i in list_v:
            url = 'http://222.73.34.165:88/student/schapter.aspx?chapterid=%s' % re.search('\d+', i).group()
            url_list.append(url)

        for url in url_list:
            t = threading.Thread(target=func, args=(url, cookies_dict, headers, user))
            t.start()

        response.status = True
        return JsonResponse(response.__dict__)


def course_detail(request, s1):
    """
    展示课程详细
    :param request:
    :param s1:
    :return:
    """
    if request.method == 'GET':
        course_id = s1
        username = request.session['username']

        print(course_id)

        cookies_dict_obj = models.UserProfile.objects.filter(username=username).first()
        password = cookies_dict_obj.pwd
        cookies_dict = eval(cookies_dict_obj.user_cookies)

        course_url = '%s/student/scourse.aspx?courseid=%s' % (config.school_url, course_id)
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0",
                   "Connection": "close", "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Upgrade-Insecure-Requests": "1",
                   'Referer': 'http://222.73.34.165:88/student/allcourse.aspx'}
        print(course_url)

        r3 = requests.get(url=course_url,
                          headers=headers,
                          cookies=cookies_dict)
        # print(r3.text)

        soup = BeautifulSoup(r3.text, 'html.parser')

        try:
            table_list = soup.find_all(name='table')[-1]
        except Exception as e:
            data = [{'t1': '该课程已修完'}]
            return render(request, 'course_detail.html', {'data': data})

        tr_list = table_list.find_all(name='tr')

        i = 0
        data = []
        for line in tr_list:
            try:
                t1 = line.find(id='coursechapters_Label9_%s' % i).text
            except Exception as e:
                data = [{'t1': '该课程已修完'}]
                return render(request, 'course_detail.html', {'data': data})
            t2 = line.find(id='coursechapters_Label11_%s' % i).text
            t3 = line.find(id='coursechapters_HyperLink3_%s' % i).get('onclick')
            t4 = line.find(name='img').get('src')
            i += 1
            data.append({'t1': t1, 't2': t2, 't3': t3, 't4': t4})

        request.session['cookies_dict'] = cookies_dict
        request.session['headers'] = headers

        return render(request, 'course_detail.html', {'data': data})


def dashboard(request):
    """
    index页面
    :param request:
    :return:
    """
    if request.method == 'GET':
        username = request.session['username']
        cookies_dict_obj = models.UserProfile.objects.filter(username=username).first()
        password = cookies_dict_obj.pwd
        cookies_dict = eval(cookies_dict_obj.user_cookies)

        data = all_course(request, username, password, cookies_dict)

        return render(request, 'index.html', {'data': data})

    return render(request, 'index.html')


def acc_login(request):
    """
    尝试登陆学校服务器 拿cookies
    :param request:
    :return:
    """
    err_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # username = '26160554'
        # password = 'B'
        if '26160500' < username < '26160580':
            pass
        else:
            err_msg = '暂不支持该学号..'
            return render(request, 'login.html', {'err_msg': err_msg})

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

        soup1 = BeautifulSoup(response.text, 'html.parser')
        user = soup1.find(id='username').text
        request.session['user'] = user

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
        # requests.session['s1'] = s1
        # requests.session['s2'] = s2
        data = all_course(request, username, password, cookies_dict)
        return render(request, 'index.html', {'data': data})

    return render(request, 'login.html', {'err_msg': err_msg})
