# _*_ coding: utf-8 _*_
__author__ = 'Keeten_Qiu'
__date__ = '2018/9/14 上午11:05'

import xadmin
from .models import *


class CourseOrgAdmin(object):
    list_display =['name' ,'desc','click_nums', 'fav_nums', 'image', 'address','city']
    search_fields =['name' ,'desc','click_nums', 'fav_nums', 'image', 'address','city']
    list_filter =['name' ,'desc','click_nums', 'fav_nums', 'image', 'address','city']

    # 设置管理页面中下拉菜单字段中可以使用自动搜索功能
    relfield_style = 'fk-ajax'




class TeacherAdmin(object):
    list_display = ['org','name', 'work_years','work_company', 'work_position','point', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org','name', 'work_years','work_company', 'work_position','point', 'click_nums', 'fav_nums']
    list_filter = ['org','name', 'work_years','work_company', 'work_position','point', 'click_nums', 'fav_nums', 'add_time']
    model_icon = 'fa fa-user-o'


class CityDictAdmin(object):
    list_display = ['name' ,'desc','add_time']
    search_fields = ['name' ,'desc']
    list_filter = ['name' ,'desc','add_time']
    model_icon = 'fa fa-location-arrow'


xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CityDict,CityDictAdmin)
