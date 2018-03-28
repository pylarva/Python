import requests
from conf import config
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect


def dashboard(request):
    return render(request, 'index.html')


def acc_login(request):
    err_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
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
                                       'username': '26160554',
                                       'pwd': 'Bingo_1991',
                                       'gtpath': ''},
                                 cookies=r1_cookies_dict)
        # print(response.text)
        r2_cookies_dict = response.cookies.get_dict()
        cookies_dict.update(r1_cookies_dict)
        cookies_dict.update(r2_cookies_dict)

        r3 = requests.post(url='%s/student/allcourse.aspx' % config.school_url,
                           data={'__VIEWSTATE': s1,
                                 '__VIEWSTATEGENERATOR': s2,
                                 '__EVENTTARGET': '',
                                 '__EVENTARGUMENT': '',
                                 'Button1': '确认登陆',
                                 'username': '26160554',
                                 'pwd': 'Bingo_1991',
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
            print('==================')
            print(title.text)
            print(i.find(name='a').get('href'))
            print(i.find(name='img').get('src'))
            course_dict['title'] = title.text
            course_dict['url'] = i.find(name='a').get('href')
            course_dict['img'] = '%s%s' % (config.school_url, i.find(name='img').get('src').split('..')[1])
            data.append(course_dict)
        return render(request, 'index.html', {'data': data})

    return render(request, 'login.html', {'err_msg': err_msg})
