# _*_ coding: utf-8 _*_
__author__ = 'Keeten_Qiu'
__date__ = '2018/9/30 下午1:52'


from django.conf.urls import url
from course.views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentsView,VideoPlayView

app_name = 'course'

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='course_detail'),
    # 课程视频列表页
    url(r'^info/(?P<course_id>\d+)$', CourseInfoView.as_view(), name='course_info'),
    # 课程评论页面
    url(r'^comment/(?P<course_id>\d+)$', CourseCommentView.as_view(), name='course_comment'),
    # 添加课程评论
    url(r'^add_comment/$', AddCommentsView.as_view(), name='add_comment'),
    # 课程视频页面
    url(r'video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),
]