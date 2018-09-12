# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from django.db import models
from datetime import  datetime

# Create your models here.


class Course(models.Model):
    name = models.CharField('课程名',max_length=50)
    desc = models.CharField('课程描述',max_length=300)
    detail = models.TextField('课程详情')
    degree = models.CharField(choices=(('cj','初级'),('zj','中级'),('gj','高级')),max_length=2)
    learn_times = models.IntegerField('学习时长(分钟)',default=0)
    students = models.IntegerField('学习人数',default=0)
    fav_nums = models.IntegerField('收藏人数',default=0)
    image = models.ImageField('封面图',upload_to='course/%Y/%m',max_length=100)
    click_nums = models.IntegerField('点击数',default=0)
    add_time = models.DateTimeField('添加时间',default=datetime.now)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name



