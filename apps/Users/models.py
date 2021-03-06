from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# 继承自django auth里面的users字段
class UserProfile(AbstractUser):
    '''用户信息表'''
    nickname = models.CharField('昵称', max_length=32, default='')
    birthday = models.DateField('生日', blank=True, null=True)
    gender = models.CharField('性别', choices=(('Male', '男'), ('Female', '女')), max_length=10, default='Female')
    address = models.CharField('地址', max_length=200, default=u'')
    mobile = models.CharField('手机号', max_length=11, null=True, blank=True)
    image = models.ImageField('头像', upload_to='image/%Y/%m', default=u'image/default.png', max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def get_unread_nums(self):
        # 获取用户未读消息的数量
        from operation.models import UserMessage
        # import放在方法里面表示调用方法的时候才去import
        # 查找该用户的未读信息,并返回数量
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    '''验证码'''
    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField('验证码的类型', choices=(('register', '注册'), ('forget', '找回密码'), ('update_email', '修改邮箱')),
                                 max_length=20)
    send_time = models.DateTimeField('发送时间', default=datetime.now)

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    '''轮播图'''
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('轮播图', upload_to='banner/%Y/%m', max_length=100)
    url = models.URLField('访问地址', max_length=200)
    index = models.IntegerField('轮播图的顺序', default=100)
    add_time = models.DateTimeField('添加的时间', default=datetime.now)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
