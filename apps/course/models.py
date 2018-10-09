# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField


# Create your models here.



class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name='课程机构',null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField('课程名', max_length=50)
    desc = models.CharField('课程描述', max_length=300)
    # detail = models.TextField('课程详情') 这个是原来的字段，将改为下面的使用富文本作为字段
    detail = UEditorField('课程详情',width=900, height=400, toolbars="full", imagePath="courses/ueditor/",
                                 filePath="courses/ueditor/", default='')
    is_banner = models.BooleanField('是否轮播',default=False)
    teacher = models.ForeignKey(Teacher,verbose_name='讲师',null=True,blank=True,on_delete=models.CASCADE)
    degree = models.CharField('课程难度', choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2)
    learn_times = models.IntegerField('学习时长(分钟)', default=0)
    students = models.IntegerField('学习人数', default=0)
    fav_nums = models.IntegerField('收藏人数', default=0)
    image = models.ImageField('封面图', upload_to='course/%Y/%m', max_length=100)
    click_nums = models.IntegerField('点击数', default=0)
    category = models.CharField('课程类别', max_length=30,default='后端开发')
    tag = models.CharField('课程标签',max_length=10,default='')
    youneed_know = models.CharField('课程需知',max_length=300,default='')
    teacher_tell = models.CharField('老师告诉你学到什么',max_length=300,default='')
    add_time = models.DateTimeField('添加时间', default=datetime.now)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程的章节数,反向取Lesson表里面的数据
        return self.lesson_set.all().count()
    get_zj_nums.short_description = '章节数'


    # 定义一个跳转方法，并展示在xadmin的管理页面，首先在class下定义一个跳转的方法
    def go_to(self):
        from django.utils.safestring import mark_safe
        # mark_safe函数的作用是告诉服务器这个连接安全并转换成url连接，否则返回a标签的文本格式
        return mark_safe('<a href="http://www.baidu.com">跳转</a>')
    go_to.short_description = '链接'

    # 获取学习人数
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    # 获取课程章节列表
    def get_course_lesson(self):
        return self.lesson_set.all()

# 设置2个页面管理同一张表的方法,第一步在models下新建class 并继承需要显示的父类
class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey('Course', verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField('章节名', max_length=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    # 获取每个章节的所有视频
    def get_lesson_video(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey('Lesson', verbose_name='章节', on_delete=models.CASCADE)
    name = models.CharField('视频名称', max_length=100)
    url = models.CharField('访问路径',max_length=200,default='')
    learn_times = models.IntegerField('学习时长(分钟)', default=0)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey('Course', verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField('名称', max_length=100)
    download = models.FileField('资源文件', upload_to='course/resource/%Y/%m', max_length=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
