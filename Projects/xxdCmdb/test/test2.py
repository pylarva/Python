#!/usr/bin/env python
# coding: utf-8

import smtplib
from email.mime.text import MIMEText
import os
import argparse
import logging
import datetime

mail_host = 'smtp.partner.outlook.cn'
mail_port = 587
mail_user = 'monitor@xinxindai.com'
mail_pass = 'Yhblsqt520'
mail_postfix = 'xinxindai.com'


def send_mail(mail_to='lichengbing@xinxindai.com',subject='ssss',content='222'):
    #me = mail_user+"<"+mail_user+"@"+mail_postfix+">"
    me = mail_user
    msg = MIMEText(content,'html','utf-8')
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = mail_to
    global sendstatus
    global senderr
    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_host,mail_port)
        smtp.starttls()
        smtp.login(mail_user,mail_pass)
        #print mail_user,mail_to,msg.as_string()
        smtp.sendmail(me,mail_to,msg.as_string())
        smtp.close()
        print('send ok')
        sendstatus = True
    except Exception as e:
        senderr = str(e)
        print(senderr)
        sendstatus = False


def logwrite(sendstatus,mail_to,content):
    logpath = '/tmp/zabbix_alert'
    if not sendstatus:
        content = senderr
    if not os.path.isdir(logpath):
        os.makedirs(logpath)

    t = datetime.datetime.now()
    daytime = t.strftime('%Y-%m-%d')
    daylogfile = logpath+'/mail_'+str(daytime)+'.log'
    logging.basicConfig(filename=daylogfile,level=logging.DEBUG)
    logging.debug(str(t)+' mail send to {0},content is: \n {1}'.format(mail_to,content))


# if __name__ == "__main__":
# if 1:
parser = argparse.ArgumentParser(description='Send mail to user for zabbix alerting')
parser.add_argument('mail_to',action="store",help='The address of E-mail that send to user')
parser.add_argument('subject',action="store",help='The E-mail subject')
parser.add_argument('content',action="store",help='The E-mail content')
args = parser.parse_args()
mail_to = args.mail_to
subject = args.subject
content = args.content
print(111)

    # send_mail(mail_to,subject,content)
send_mail()
    # send_mail(mail_to='lichengbing@xinxindai.com', subject='sss', content='1111')
    # logwrite(sendstatus,mail_to,content)