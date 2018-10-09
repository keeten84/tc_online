# _*_ coding: utf-8 _*_
__author__ = 'Keeten_Qiu'
__date__ = '2018/9/13 下午3:41'

import xadmin
from .models import Course, Lesson, Video, CourseResource, BannerCourse


# 组装页面的方法
class LessonInLine(object):
    model = Lesson
    extra = 0


# 组装页面的方法
class CourseResourceInLine(object):
    model = CourseResource
    extra = 0




class CourseAdmin(object):
    list_display = ['name', 'course_org', 'desc', 'detail', 'degree',
                    'learn_times', 'students', 'click_nums','get_zj_nums','go_to']

    search_fields = ['name', 'desc', 'detail', 'degree',
                     'learn_times', 'students', 'fav_nums',
                     'image', 'click_nums']

    list_filter = ['name', 'course_org', 'desc', 'detail', 'degree',
                   'learn_times', 'students', 'fav_nums',
                   'image', 'click_nums', 'add_time']
    # 设置管理页面的图标
    model_icon = 'fa fa-list'
    # 设置进入该管理页面下的默认排序的方法
    ordering = ['-click_nums']
    # 设置某些字段不可以从页面中修改的方法
    readonly_fields = ['click_nums']
    # 设置某些字段在管理页面中不显示的方法,如果设置了readonly，该字段无法设置exclude
    exclude = ['fav_nums']
    # 设置管理页面中下拉菜单字段中可以使用自动搜索功能，比如course_org机构名，需要到机构的Admin中去设置
    # 组装其他管理页面
    inlines = [LessonInLine, CourseResourceInLine]
    # 直接在管理页面列表页中可以编辑该字段的数据的方法
    list_editable = ['degree','desc']
    # 设置自动刷新时间
    refresh_times = [3, 5]
    # 注册ueditor到页面
    style_fields = {'detail': 'ueditor'}
    # 导入excel插件
    import_excel = True

    # 设置2个页面管理同一张表的方法，第三步，将父类的数据去出子类的数据，避免重复显示
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner = False)
        return qs


    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin,self).post(request, *args, **kwargs)


# 设置2个页面管理同一张表的方法，第二步，复制父类的Admin类容，并重构queryset方法
class BannerCourseAdmin(object):
    list_display = ['name', 'course_org', 'desc', 'detail', 'degree','learn_times', 'students', 'click_nums']
    search_fields = ['name', 'desc', 'detail', 'degree','learn_times', 'students', 'fav_nums','image', 'click_nums']
    list_filter = ['name', 'course_org', 'desc', 'detail', 'degree','learn_times', 'students', 'fav_nums','image', 'click_nums', 'add_time']
    model_icon = 'fa fa-list'
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']
    inlines = [LessonInLine, CourseResourceInLine]
    style_fields = {'detail': 'ueditor'}


    # 通过重新构造queryset方法，重新过滤需要显示的数据,过滤的数据可以根据要求自己写
    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner = True)
        return qs




class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    # course__name根据外间的name字段添加过滤器
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']
    model_icon = 'fa fa-file-movie-o'


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'download', 'add_time']
    model_icon = 'fa fa-file-zip-o'


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
