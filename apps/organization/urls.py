# _*_ coding: utf-8 _*_
__author__ = 'Keeten_Qiu'
__date__ = '2018/9/25 下午7:28'


from django.conf.urls import url
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView, \
    TeacherList, TeacherDetail

app_name = 'organization'

urlpatterns = [
    #课程机构首页的映射
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(),name='add_ask'),
    url(r'^home/(?P<org_id>\d+)$', OrgHomeView.as_view(),name='org_home'),
    url(r'^course/(?P<org_id>\d+)$', OrgCourseView.as_view(),name='org_course'),
    url(r'^desc/(?P<org_id>\d+)$', OrgDescView.as_view(),name='org_desc'),
    url(r'^org_teacher/(?P<org_id>\d+)$', OrgTeacherView.as_view(),name='org_teacher'),

    # 机构收藏功能
    url(r'^add_fav$', AddFavView.as_view(),name='add_fav'),

    # 讲师列表页
    url(r'^teacher/list$', TeacherList.as_view(),name='teacher_list'),
    # 讲师详情页
    url(r'^teacher/detail/(?P<teacher_id>\d+)$', TeacherDetail.as_view(),name='teacher_detail'),

]