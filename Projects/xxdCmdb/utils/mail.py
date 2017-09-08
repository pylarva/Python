#!/usr/bin/env python
# coding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from conf import mail_config

mail_host = 'smtp.partner.outlook.cn'
mail_port = 587
mail_user = 'monitor@xinxindai.com'
mail_pass = 'Yhblsqt520'
mail_postfix = 'xinxindai.com'


def send_mail(mail_to, subject, content):
    """
    发送邮件 不带附件
    :param mail_to:
    :param subject:
    :param content:
    :return:
    """
    me = mail_user
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = mail_host

    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_host, mail_port)
        smtp.starttls()
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(me, mail_to, msg.as_string())
        smtp.close()
        print('Email send ok...')
    except Exception as e:
        senderr = str(e)
        print(senderr)
    return True


def send_mail_attachment(mail_to, subject, content):
    """
    发送邮件 带附件
    :param mail_to:
    :param subject:
    :param content:
    :return:
    """
    me = mail_user
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = mail_host

    # msg = MIMEMultipart()
    # msg['Subject'] = Header('测试', 'utf-8')
    # msg['From'] = Header(me)
    # msg['To'] = Header(mail_host)
    # msg.attach(MIMEText('这是菜鸟教程Python 邮件发送测试……', 'plain', 'utf-8'))

    # 附件超过3M就发送不成功？？？
    att1 = MIMEText(open('/opt/config.zip', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="VpnClient.tgz"'
    msg.attach(att1)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_host, mail_port)
        smtp.starttls()
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(me, mail_to, msg.as_string())
        smtp.close()
        print('Email send ok...')
    except Exception as e:
        senderr = str(e)
        print(senderr)
    return True

# if __name__ == "__main__":
# if 1:
    # send_mail(mail_to,subject,content)
    # send_mail_attachment(mail_to='lichengbing@xinxindai.com', subject='测试01', content='1111')
    # logwrite(sendstatus,mail_to,content)