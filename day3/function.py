#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing


'''
def sendmail():
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.utils import formataddr

        msg = MIMEText('邮件内容', 'plain', 'utf-8')
        msg['From'] = formataddr(["武沛齐", 'wptawy@126.com'])
        msg['To'] = formataddr(["走人", '424662508@qq.com'])
        msg['Subject'] = "主题"

        server = smtplib.SMTP("smtp.163.com", 25)
        server.login("lichengbing9027@163.com", "li12345")
        server.sendmail('lichengbing9027@163.com', ['1326126359@qq.com', ], msg.as_string())
        server.quit()
    except:
        return False
    else:
        return True

ret = sendmail()
print(ret)
'''

# 1、普通参数（严格按照顺序，将实际参数赋值给形式参数）
# 2、默认参数（必须放置在参数列表的最后）
# 3、指定参数（将实际参数赋值给指定的形式参数）
# 4、动态参数：
#    *        默认将传入的参数，全部放置在元组中
#    **       默认将传入的参数，全部放置在列表中
# 5、万能参数 *args，**kwargs


def f1(*args):
    print(args,type(args))

# 动态参数
f1(11,22,'hhhh')  # 给全部的参数作为元组的一个元素
li = [22,33,'hehe']
f1(li,'44')
f1(*li)  # 给全部的参数作为元组的每一个元素添加
lii = 'kobe'
f1(*lii)  # 循环字符串每一个元素


def f2(**args):
    print(args,type(args))
f2(n1="kobe")
dic = {'k1':'v1','k2':'v2'}
f2(kk=dic)   # 只有一个键值对
f2(**dic)


def f3(*args,**kwargs):     # 万能参数只能放置在args后
    print(args)
    print(kwargs)
f3(11,22,33,k1="v1",k2="v2")

