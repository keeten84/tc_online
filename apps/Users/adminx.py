# _*_ coding: utf-8 _*_
_author__ = 'Keeten_Qiu'
__date__ = '2018/9/13 下午2:48'

import xadmin
from xadmin import views
from xadmin.layout import Fieldset, Main, Side, Row
from .models import EmailVerifyRecord, Banner, UserProfile


#注册管理页面的主题功能
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


#设置管理页显示的相关设置
class GlobalSettings(object):
    # 设置管理页面的名称
    site_title = '教学后台管理系统'
    # 设置页面底部公司名
    site_footer = '教学在线网'
    # 设置左边导航页自动收缩
    menu_style = 'accordion'


# 定义一个admin管理器用于管理页面显示的字段等等
class EmailVerifyRecordAdmin(object):
    #可以使用元祖()，单是要注意每个后面必须家逗号，不然会报错
    list_display = ['code','email','send_type','send_time']
    #在管理页面添加搜索功能
    search_fields = ['code','email','send_type']
    #在管理页面添加过滤器
    list_filter = ['code','email','send_type','send_time']
    model_icon = 'fa fa-envelope-o'


class BannerAdmin(object):
    list_display = ['title' ,'image' ,'url' ,'index','add_time']
    search_fields = ['title' ,'image' ,'url' ,'index']
    list_filter = ['title' ,'image' ,'url' ,'index','add_time']
    # 设置管理页面的图标
    model_icon = 'fa fa-file-image-o'

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)   #注册管理页面的主题功能
xadmin.site.register(views.CommAdminView,GlobalSettings)#注册管理页面显示功能设置

