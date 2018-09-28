# _*_ coding: utf-8 _*_
__author__ = 'Keeten_Qiu'
__date__ = '2018/9/14 下午11:45'
from django import forms
from captcha.fields import CaptchaField



# forms.py文件的作用：存储form定义的文件

class LoginForm(forms.Form):
    # 注意变量名必须和前端页面的input中的name相同，否则不会做验证
    username = forms.CharField(required=True)
    #判断密码如果少于5为数则不会进行验证
    password = forms.CharField(required=True,min_length=5)


# 对注册表单的验证
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=6)
    # 添加验证码的验证，添加error_messages，可以自定义抛出错误的提示
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


# 对忘记密码表单的验证
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


# 重置密码表单的验证
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=6)
    password2 = forms.CharField(required=True,min_length=6)