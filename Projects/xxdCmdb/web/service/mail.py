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


# parser = argparse.ArgumentParser(description='Send mail to user for zabbix alerting')
# parser.add_argument('mail_to',action="store",help='The address of E-mail that send to user')
# parser.add_argument('subject',action="store",help='The E-mail subject')
# parser.add_argument('content',action="store",help='The E-mail content')
# args = parser.parse_args()
# mail_to = args.mail_to
# subject = args.subject
# content = args.content

# mail_to = 'lichengbing@xinxindai.com'
# subject = 'sss'
# content = 'ttt'


def send_mail(mail_to, subject, content):
    me = mail_user
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = mail_host
    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_host,mail_port)
        smtp.starttls()
        smtp.login(mail_user,mail_pass)
        smtp.sendmail(me, mail_to, msg.as_string())
        smtp.close()
        print('Email send ok...')
    except Exception as e:
        senderr = str(e)
        print(senderr)
        sendstatus = False
    return True



# if __name__ == "__main__":
# if 1:


    # send_mail(mail_to,subject,content)
    # send_mail(mail_to='lichengbing@xinxindai.com', subject='sss', content='1111')
    # logwrite(sendstatus,mail_to,content)