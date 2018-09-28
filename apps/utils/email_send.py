# _*_ coding: utf-8 _*_
from random import Random

__author__ = 'Keeten_Qiu'
__date__ = '2018/9/15 上午2:50'

from Users.models import EmailVerifyRecord
from django.core.mail import send_mail
from MxOnline.settings import EMAIL_FROM



# 生成随机字符从方法
def generate_random_str(randomlegth=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlegth):
        str += chars[random.randint(0, length)]
    return str


# 发送邮箱验证码
def send_register_email(email,send_type='register'):
    '''参数分别是email和发送验证码类型（注册/找回密码）'''

    # 实例化EmailVertiyRecode表
    email_record = EmailVerifyRecord()
    # 生成16w位随机字符串
    code = generate_random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    # 以上步骤先将验证码保存到数据库中，以便核对邮箱和数据库到验证码一致
    email_title = ''
    email_body = ''
    if send_type == 'register':
        email_title = '暮学在线网注册激活连接'
        email_body = '请点击下面的连接激活您的账号： http://127.0.0.1:8000/active/{0}'.format(code)
        # 发送邮件 使用from django.core.mail import send_mail 方法发送
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email], fail_silently=False)
        if send_status:
            print('发送邮件成功')

    elif send_type == 'forget':
        email_title = '暮学在线网密码重置连接'
        email_body = '请点击下面的连接重置您的密码： http://127.0.0.1:8000/reset/{0}'.format(code)
        # 发送邮件 使用from django.core.mail import send_mail 方法发送
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email], fail_silently=False)
        if send_status:
            print('发送邮件成功')






