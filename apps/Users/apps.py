# _*_ coding:utf-8 _*_
from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'Users'
    #修改管理页面显示中文
    verbose_name = '用户信息'
