# !/usr/bin/env python
# -*- coding:utf-8 -*-

s = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>

</title><link href="../css/main.css" rel="stylesheet" type="text/css" />
    <style type="text/css">
        .style1
        {
            text-align: center;
            width:150px;
            overflow:hidden;
        }
    </style>
        <script type="text/javascript">

            if (top == self) {
                window.location.href = "../login.aspx?gtpage=student/allcourse.aspx";
            }
            </script>
</head>
<body>
    <form method="post" action="./allcourse.aspx" id="form1">
<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="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" />

<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="B37BC03C" />
    <div>

        欢迎你，<span id="username">黎承兵</span>
    &nbsp;(<span id="hier">专升本</span>
        &nbsp;- <span id="spoint">校内</span>
        )</div>
    <p>
        您目前参加的课程有：(点击课程，进入学习)<br />
        <table id="learnedlist" cellspacing="20">
	<tr>
		<td>
                <div class="style1">
                <a id="learnedlist_HyperLink2_0" href="scourse.aspx?courseid=29"><img id="learnedlist_ImageButton1_0" src="../files/CourseDocs/29/20131028100217.png" alt="并行程序设计" height="120" width="90" />
                    <br />
                    <span id="learnedlist_LinkButton1_0">并行程序设计</span><br />
                         （<span id="learnedlist_Label2_0">专升本</span>）
                    </a>
                </div>
            </td><td>
                <div class="style1">
                <a id="learnedlist_HyperLink2_2" href="scourse.aspx?courseid=98"><img id="learnedlist_ImageButton1_2" src="../files/CourseDocs/98/20124807050639.bmp" alt="Ｃ 语言程序设计" height="120" width="90" />
                    <br />
                    <span id="learnedlist_LinkButton1_2">Ｃ 语言程序设计</span><br />
                         （<span id="learnedlist_Label2_2">专升本</span>）
                    </a>
                </div>
            </td><td>
                <div class="style1">
                <a id="learnedlist_HyperLink2_4" href="scourse.aspx?courseid=134"><img id="learnedlist_ImageButton1_4" src="../files/CourseDocs/134/20131727110524.jpg" alt="计算机组成原理" height="120" width="90" />
                    <br />
                    <span id="learnedlist_LinkButton1_4">计算机组成原理</span><br />
                         （<span id="learnedlist_Label2_4">专升本</span>）
                    </a>
                </div>
            </td><td>
                <div class="style1">
                <a id="learnedlist_HyperLink2_6" href="scourse.aspx?courseid=49"><img id="learnedlist_ImageButton1_6" src="../files/CourseDocs/default/nopic.gif" alt="公共系列讲座" height="120" width="90" />
                    <br />
                    <span id="learnedlist_LinkButton1_6">公共系列讲座</span><br />
                         （<span id="learnedlist_Label2_6">专升本</span>）
                    </a>
                </div>
            </td><td>
                <div class="style1">
                <a id="learnedlist_HyperLink2_8" href="scourse.aspx?courseid=142"><img id="learnedlist_ImageButton1_8" src="../files/CourseDocs/142/20141714110119.jpg" alt="计算机英语" height="120" width="90" />
                    <br />
                    <span id="learnedlist_LinkButton1_8">计算机英语</span><br />
                         （<span id="learnedlist_Label2_8">专升本</span>）
                    </a>
                </div>
            </td>
	</tr><tr>
		<td>
                <div class="style1">
                <a id="learnedlist_HyperLink2_1" href="scourse.aspx?courseid=70"><img id="learnedlist_ImageButton1_1" src="../files/CourseDocs/70/20115219010958.jpg" alt="马克思主义基本原理概论" height="120" width="90" />
                    <br />
                    <span id="learnedlist_LinkButton1_1">马克思主义基本原理概论</span><br />
                         （<span id="learnedlist_Label2_1">专升本</span>）
                    </a>
                </div>
            </td><td>
                <div class="style1">
                <a id="learnedlist_HyperLink2_3" href="scourse.aspx?courseid=121"><img id="learnedlist_ImageButton1_3" src="../files/CourseDocs/121/20143207080738.jpg" alt="Web实用技术" height="120" width="90" />
                    <br />
                    <span id="learnedlist_LinkButton1_3">Web实用技术</span><br />
                         （<span id="learnedlist_Label2_3">专升本</span>）
                    </a>
                </div>
            </td><td>
                <div class="style1">
                <a id="learnedlist_HyperLink2_5" href="scourse.aspx?courseid=43"><img id="learnedlist_ImageButton1_5" src="../files/CourseDocs/default/nopic.gif" alt="实用英语写作" height="120" width="90" />
                    <br />
                    <span id="learnedlist_LinkButton1_5">实用英语写作</span><br />
                         （<span id="learnedlist_Label2_5">专升本</span>）
                    </a>
                </div>
            </td><td>
                <div class="style1">
                <a id="learnedlist_HyperLink2_7" href="scourse.aspx?courseid=85"><img id="learnedlist_ImageButton1_7" src="../files/CourseDocs/default/nopic.gif" alt="云计算技术" height="120" width="90" />
                    <br />
                    <span id="learnedlist_LinkButton1_7">云计算技术</span><br />
                         （<span id="learnedlist_Label2_7">专升本</span>）
                    </a>
                </div>
            </td><td></td>
	</tr>
</table>
    </p>
    <p>
        开始新的课程：<br />
        <table id="alllist" cellspacing="20">
	<tr>
		<td>
                <div class="style1">
                    <a id="alllist_HyperLink1_0" href="scourse.aspx?courseid=135"><img id="alllist_Image1_0" src="../files/CourseDocs/default/nopic.gif" alt="计算机专业概论" height="120" width="90" /><br />

                   <span id="alllist_Label1_0">计算机专业概论</span><br />
                       （<span id="alllist_Label2_0">专升本</span>）
                   </a>
                </div>
            </td><td>
                <div class="style1">
                    <a id="alllist_HyperLink1_2" href="scourse.aspx?courseid=137"><img id="alllist_Image1_2" src="../files/CourseDocs/default/nopic.gif" alt="数据仓库与数据挖掘" height="120" width="90" /><br />

                   <span id="alllist_Label1_2">数据仓库与数据挖掘</span><br />
                       （<span id="alllist_Label2_2">专升本</span>）
                   </a>
                </div>
            </td><td>
                <div class="style1">
                    <a id="alllist_HyperLink1_4" href="scourse.aspx?courseid=159"><img id="alllist_Image1_4" src="../files/CourseDocs/default/nopic.gif" alt="专业课程精选" height="120" width="90" /><br />

                   <span id="alllist_Label1_4">专业课程精选</span><br />
                       （<span id="alllist_Label2_4"></span>）
                   </a>
                </div>
            </td><td>
                <div class="style1">
                    <a id="alllist_HyperLink1_6" href="scourse.aspx?courseid=214"><img id="alllist_Image1_6" src="../files/CourseDocs/default/nopic.gif" alt="专业概论及学科前沿介绍" height="120" width="90" /><br />

                   <span id="alllist_Label1_6">专业概论及学科前沿介绍</span><br />
                       （<span id="alllist_Label2_6">专升本</span>）
                   </a>
                </div>
            </td><td>
                <div class="style1">
                    <a id="alllist_HyperLink1_8" href="scourse.aspx?courseid=222"><img id="alllist_Image1_8" src="../files/CourseDocs/default/nopic.gif" alt="计算机新技术讲座" height="120" width="90" /><br />

                   <span id="alllist_Label1_8">计算机新技术讲座</span><br />
                       （<span id="alllist_Label2_8">专升本</span>）
                   </a>
                </div>
            </td>
	</tr><tr>
		<td>
                <div class="style1">
                    <a id="alllist_HyperLink1_1" href="scourse.aspx?courseid=136"><img id="alllist_Image1_1" src="../files/CourseDocs/default/nopic.gif" alt="计算机学科前沿技术介绍" height="120" width="90" /><br />

                   <span id="alllist_Label1_1">计算机学科前沿技术介绍</span><br />
                       （<span id="alllist_Label2_1">专升本</span>）
                   </a>
                </div>
            </td><td>
                <div class="style1">
                    <a id="alllist_HyperLink1_3" href="scourse.aspx?courseid=138"><img id="alllist_Image1_3" src="../files/CourseDocs/default/nopic.gif" alt="生物认证技术" height="120" width="90" /><br />

                   <span id="alllist_Label1_3">生物认证技术</span><br />
                       （<span id="alllist_Label2_3">专升本</span>）
                   </a>
                </div>
            </td><td>
                <div class="style1">
                    <a id="alllist_HyperLink1_5" href="scourse.aspx?courseid=197"><img id="alllist_Image1_5" src="../files/CourseDocs/197/20142930030601.jpg" alt="软件工程与实践" height="120" width="90" /><br />

                   <span id="alllist_Label1_5">软件工程与实践</span><br />
                       （<span id="alllist_Label2_5">专升本</span>）
                   </a>
                </div>
            </td><td>
                <div class="style1">
                    <a id="alllist_HyperLink1_7" href="scourse.aspx?courseid=219"><img id="alllist_Image1_7" src="../files/CourseDocs/default/nopic.gif" alt="计算机专业概论及学科前沿介绍" height="120" width="90" /><br />

                   <span id="alllist_Label1_7">计算机专业概论及学科前沿介绍</span><br />
                       （<span id="alllist_Label2_7">专升本</span>）
                   </a>
                </div>
            </td><td>
                <div class="style1">
                    <a id="alllist_HyperLink1_9" href="scourse.aspx?courseid=258"><img id="alllist_Image1_9" src="../files/CourseDocs/default/nopic.gif" alt="通识课" height="120" width="90" /><br />

                   <span id="alllist_Label1_9">通识课</span><br />
                       （<span id="alllist_Label2_9">专升本</span>）
                   </a>
                </div>
            </td>
	</tr>
</table>
    </p>
    </form>
    </body>
    <script src="/WebResource.axd?d=g6YGCwmmOZ6ToR5cAznB-pdLKoPpemIuoFKJbCJoCBrUiUz9Vj_wShbMCvOP1TT25Ori6ykmXxCPHNKuDGLspKkoKe4CUADR_NlZTyiyra81&amp;t=636396566200000000" type="text/javascript"></script>
</html>"""

from bs4 import BeautifulSoup
#
soup = BeautifulSoup(s, 'html.parser')
#
# td_list = soup.find(id='learnedlist').find_all(name='td')
# for i in td_list:
#     title = i.find(name='span')
#     if not title:
#         continue
#     print('==================')
#     print(title.text)
#     print(i.find(name='a').get('href'))
#     print(i.find(name='img').get('src'))

# s1 = '../files/CourseDocs/default/nopic.gif'
# s2 = s1.split('..')[1]
# print(s2)

# 线程 进程
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

url_list = ['www.baidu.com', 'http://www.google.com.hk']

def task(url):
    response = requests.get(url)
    print(response.content)

# pool = ThreadPoolExecutor(10)
pool = ProcessPoolExecutor(10)

for url in url_list:
    pool.submit(task, url)

pool.shutdown(wait=True)