# _*_ coding: utf-8 _*_
__author__ = 'Keeten_Qiu'
__date__ = '2018/10/1 下午11:45'


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class LoginRequiredMixin(object):
    '''提前对用户的登录信息做验证，当view视图函数继承这个类之后，如果用户没有登录，就跳转到login登录页面'''
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)