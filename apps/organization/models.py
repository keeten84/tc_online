# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from django.db import models
from datetime import datetime


class CourseOrg(models.Model):
    name = models.CharField('机构名称',max_length=50)
    desc = models.TextField('机构描述')
    tag = models.CharField('机构标签',default='全国知名',max_length=10)
    category = models.CharField('机构类别',max_length=20,choices=(('pxjg','培训机构'),('gr','个人'),('gx','高校')),default='pxjg')
    click_nums = models.IntegerField('点击数',default=0)
    fav_nums = models.IntegerField('收藏数',default=0)
    image = models.ImageField('机构logo',upload_to='org/%Y/%m',max_length=100)
    address = models.CharField('机构地址',max_length=200)
    city = models.ForeignKey('CityDict',verbose_name='城市名',on_delete=models.CASCADE)
    students = models.IntegerField('学习人数',default=0)
    course_nums = models.IntegerField('课程数',default=0)
    add_time = models.DateTimeField('添加时间',default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机构列表'
        verbose_name_plural = verbose_name


    # 获取课程机构的教师数量
    def get_teacher_nums(self):
        return self.teacher_set.all().count()





class Teacher(models.Model):
    org = models.ForeignKey('CourseOrg',verbose_name='所属机构名',on_delete=models.CASCADE)
    name = models.CharField('授课教师', max_length=10)
    age = models.CharField('年龄',max_length=3,default=18)
    work_years = models.IntegerField('工作年限',default=0)
    work_company = models.CharField('就职公司',max_length=50)
    work_position = models.CharField('工作职位',max_length=50)
    point = models.CharField('教学特点',max_length=50)
    click_nums = models.IntegerField('点击数', default=0)
    fav_nums = models.IntegerField('收藏数', default=0)
    add_time = models.DateTimeField('添加时间', default=datetime.now)
    image = models.ImageField('头像', upload_to='teacher/%Y/%m', max_length=100,default='')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def get_course_nums(self):
        '''反向查询课程数量，因为course有外键跟teacher相关联'''
        return self.course_set.all().count()


class CityDict(models.Model):
    name = models.CharField('城市名', max_length=50)
    desc = models.CharField('描述',max_length=200)
    add_time =models.DateTimeField('添加时间',default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

