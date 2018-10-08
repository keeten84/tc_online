# _*_ coding: utf-8 _*_


__author__ = 'Keeten_Qiu'
__date__ = '2018/10/4 下午8:09'

from django.conf.urls import url
from Users.views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, \
    MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

app_name = 'Users'

urlpatterns = [
    # 用户信息页面
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 用户个人信息中心中，用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    # 用户个人中心中修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    # 用户个人中心修改邮箱发送验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    # 用户个人中心，我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    # 用户个人中心，我收藏的个人机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),
    # 用户个人中心，我收藏的老师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
    # 用户个人中心，我收藏的公开课
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),
    # 用户个人中心，我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),
]