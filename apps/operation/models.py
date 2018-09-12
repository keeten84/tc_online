# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from Users.models import UserProfile
from course.models import Course

# Create your models here.
class UserAsk(models.Model):
    '''用户咨询'''
    name = models.CharField('用户名',max_length=20)
    mobile = models.CharField('手机',max_length=11)
    course_name = models.CharField('课程名称',max_length=50)
    add_time = models.DateTimeField('添加时间',default=datetime.now)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    '''课程评论'''
    user = models.ForeignKey(UserProfile,verbose_name='用户',on_delete=models.CASCADE)
    course = models.ForeignKey(Course,verbose_name='课程',on_delete=models.CASCADE)
    comment= models.CharField('评论',max_length=200)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    fav_id = models.IntegerField('数据id',default=0)
    fav_type = models.IntegerField(choices=((1,'课程'),(2,'课程机构'),(3,'讲师')),default=1,verbose_name='收藏类型')
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField('接收用户',default=0)
    message = models.CharField('消息内容',max_length=500)
    has_read = models.BooleanField('是否已读',default=False)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural =  verbose_name


class UserCourse(models.Model):
    '''用户学习的课程'''
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = '用户学习的课程'
        verbose_name_plural = verbose_name