# _*_ coding: utf-8 _*_
__author__ = 'Keeten_Qiu'
__date__ = '2018/9/25 下午7:19'
import re
from django import forms
from operation.models import UserAsk


# 使用ModelForm定义forms的方法
class UserAskForm(forms.ModelForm):
    # 创建一个Meta类指出是由哪个model直接转换的
    class Meta:
        model = UserAsk
        # 指定我需要验证的字段
        fields = ['name','mobile','course_name']

    # 添加自定义的表单验证的方法,定义后当提交表单的时候会自动调用这个方法
    def clean_mobile(self):
        '''
        验证手机号码是否合法
        '''
        mobile = self.cleaned_data['mobile']
        # 手机的正则表达式，上网可以查找到
        REGEX_MOBILE = "^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$"
        p = re.compile(REGEX_MOBILE)
        # 判断输入的手机号码是否能匹配正则表达式
        if p.match(mobile):
            # 能匹配返回手机号码
            return mobile
        else:
            # 不能匹配则报错
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")