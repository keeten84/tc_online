# _*_ coding: utf-8 _*_
__author__ = 'Keeten_Qiu'
__date__ = '2018/9/14 上午11:08'

import xadmin
from .models import *


class UserAskAdmin(object):
    list_display = ['name', 'mobile','course_name','add_time']
    search_fields = ['name', 'mobile','course_name']
    list_filter = ['name', 'mobile','course_name','add_time']
    model_icon = 'fa fa-question-circle'


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comment', 'add_time']
    search_fields = ['user', 'course', 'comment']
    list_filter = ['user', 'course', 'comment', 'add_time']
    model_icon = 'fa fa-comments'



class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields =  ['user', 'fav_id', 'fav_type']
    list_filter =  ['user', 'fav_id', 'fav_type', 'add_time']
    model_icon = 'fa fa-star'


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']
    model_icon = 'fa fa-commenting-o'



class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']
    model_icon = 'fa fa-book'



xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)







list_display = ['name' ,'desc','add_time']
search_fields = ['name' ,'desc']
list_filter = ['name' ,'desc','add_time']