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

# str.format() 格式化输出
s1 = "i am {0}, age {1}".format("kobe",18)
print(s1)
s2 = "i am {0}, age {1}".format(*["kobe",18])
print(s2)
s3 = "i am {name}, age {age}".format(name='kobe',age='18')
print(s3)
dic_01 = {'name':'kobe','age':18}
s4 = "i am {name}, age {age}".format(**dic_01)
print(s4)


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


# 函数扩展01，重复函数定义（垃圾内存将被Python回收）
def f4(a1,a2):
    return a1 + a2
def f4(a1,a2):
    return a1 * a2
ret = f4(8,8)
print(ret)


# 函数扩展02(函数传参是原值引用还是重新创建的新值？)
def f5(a1):
    a1.append(999)
li_01 = [11,22,33]
f5(li_01)
print(li_01)


# 函数扩展03
# 全局变量，所有的作用域都可读
NAME = "kobe"      # 全局变量(潜规则：全局变量都用大写)
def f6():
    age = 18       # 局部变量
    #global NAME    # 修改全局变量
# 如果需要修改的变量是一个列表，则在函数里面可以读，可以append添加，但是不可以修改或者赋值
    NAME = "jordan"
    print(NAME,age)
f6()
print(NAME)