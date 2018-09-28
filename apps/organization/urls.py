# _*_ coding: utf-8 _*_
__author__ = 'Keeten_Qiu'
__date__ = '2018/9/25 下午7:28'


from django.conf.urls import url
from .views import OrgView, AddUserAskView, OrgHomeView

app_name = 'organization'

urlpatterns = [
    #课程机构首页的映射
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(),name='add_ask'),
    url(r'^home/(?P<org_id>\d+)$', OrgHomeView.as_view(),name='org_home'),

]