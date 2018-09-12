# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from django.db import models
from datetime import datetime


class CourseOrg(models.Model):
    name = models.CharField('机构名称',max_length=50)
    desc = models.TextField('机构描述')
    click_nums = models.IntegerField('点击数',default=0)
    fav_nums = models.IntegerField('收藏数',default=0)
    image = models.ImageField('封面图',upload_to='org/%Y/%m',max_length=100)
    address = models.CharField('机构地址',max_length=200)
    city = models.ForeignKey('CityDict',verbose_name='城市名',on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '机构列表'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    org = models.ForeignKey('CourseOrg',verbose_name='所属机构名',on_delete=models.CASCADE)
    name = models.CharField('授课教师', max_length=10)
    work_years = models.IntegerField('工作年限',default=0)
    work_company = models.CharField('就职公司',max_length=50)
    work_position = models.CharField('工作职位',max_length=50)
    point = models.CharField('教学特点',max_length=50)
    click_nums = models.IntegerField('点击数', default=0)
    fav_nums = models.IntegerField('收藏数', default=0)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name


class CityDict(models.Model):
    name = models.CharField('城市名', max_length=50)
    desc = models.CharField('描述',max_length=200)
    add_time =models.DateTimeField('添加时间',default=datetime.now)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

