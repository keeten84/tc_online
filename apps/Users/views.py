import json
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.urls import reverse
from django.views.generic.base import View
from Users.forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UserInfoForm
from Users.models import UserProfile, EmailVerifyRecord, Banner
from course.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from utils.email_send import send_register_email
from apps.utils.mixin_utils import LoginRequiredMixin
from .forms import UploadImageForm
from pure_pagination import PageNotAnInteger, Paginator


class MyMessageView(LoginRequiredMixin,View):
    '''个人中心，我的消息'''
    def get(self,request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        # 补充未读消息清空的逻辑，返回前端小喇叭信息显示是否有信息未读
        # 搜索出该登录用户的未读信息
        all_unread_messages = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 4, request=request)
        messages = p.page(page)


        return render(request,'usercenter-message.html',{
            'messages':messages,
        })



class MyFavCourseView(LoginRequiredMixin,View):
    '''个人中心，我收藏的课程'''
    def get(self,request):
        courses_list=[]
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            courses_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'fav_courses': courses_list,
        })




class MyFavTeacherView(LoginRequiredMixin,View):
    '''个人中心，我收藏的机构'''
    def get(self,request):
        teacher_list=[]
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request,'usercenter-fav-teacher.html',{
            'fav_teachers':teacher_list,
        })



class MyFavOrgView(LoginRequiredMixin,View):
    '''个人中心，我收藏的机构'''
    def get(self,request):
        org_list=[]
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id = org_id)
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{
            'fav_orgs':org_list,
        })



class MyCourseView(LoginRequiredMixin,View):
    '''个人中心，我的课程'''
    def get(self,request):
        user_course = UserCourse.objects.filter(user = request.user)
        return render(request,'usercenter-mycourse.html',{
            'user_course':user_course,
        })


class UpdateEmailView(LoginRequiredMixin, View):
    '''修改邮箱逻辑'''

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"code":"验证码错误"}', content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    '''用户个人中心发送邮箱验证码'''

    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    '''用户个人中心修改密码'''

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                # js操作只能返回json格式
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success", "msg":"密码修改成功"}', content_type='application/json')
        else:
            # 如果用户操作出错，直接将form下面的errors的错误信息转化为json格式并传会前端
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    '''用户个人中心修改头像'''

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success", "msg":"已修改头像"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"修改头像操作失败"}', content_type='application/json')


class UserInfoView(LoginRequiredMixin, View):
    '''用户个人中心页面'''

    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        # 查找该用户的资料
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            # 前端页面的value必须与数据库中的字段名一致，否则无法提取前端的输入数据
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


# 重新家载authenticate，是其可以检测用邮箱登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 忘记密码的业务逻辑
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        # 实例话forgetform对象
        forget_form = ForgetForm(request.POST)
        # 如果通过Form检测
        if forget_form.is_valid():
            # 从前端获取用户的emial账号
            email = request.POST.get('email', '')
            # 发送重置密码连接
            send_register_email(email, send_type='forget')
            # 发送完毕返回提示页面，提示用户发送成功
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# 通过邮件激活用户的业务逻辑
class ActiveUserView(View):
    def get(self, request, active_code):
        # 从EmailVerifyRecode表中获取对象
        all_recodes = EmailVerifyRecord.objects.get(code=active_code)
        # 如果能够查找到对象，继续往下
        if all_recodes:
            # 从数据对象中遍历
            # for recode in all_recodes:
            # 从数据对象中获得email到数据
            email = all_recodes.email
            # 根据email数据在UserProfile中获取到用户资料
            user = UserProfile.objects.get(email=email)
            # 将激活字段从默认到False改为True
            user.is_active = True
            # 保存
            user.save()
        else:
            return render(request, 'active_fail.html')
        # 激活之后跳转到登录页面
        return render(request, 'login.html')


# 通过邮件激活用户的业务逻辑
class ResetView(View):
    def get(self, request, active_code):
        # 从EmailVerifyRecode表中获取对象
        all_recodes = EmailVerifyRecord.objects.get(code=active_code)
        # 如果能够查找到对象，继续往下
        if all_recodes:
            # 根据用户email进行查找
            email = all_recodes.email
            # 如果有就返回重置密码的页面
            return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        # return render(request,'login.html')


# 修改密码的业务逻辑
class ModifyPwdView(View):
    '''修改用户密码'''

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')

        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


# 注册功能的业务逻辑
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 从前端过去到用户名和密码
            user_name = request.POST.get('email', '')
            # 判断用户是否已经存在
            if UserProfile.objects.filter(email=user_name):
                # 如果用户已经存在，返回注册页面，并返回用户已经填写的数据和返回错误信息
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经被注册'})
            pass_word = request.POST.get('password', '')
            # 实例化UserProfile表
            user_profile = UserProfile()
            # 存储到表中
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False  # 设置用户未激活，必须通过点击发送邮件验证后才激活用户
            # 对密码加密后在保存到表中,使用from django.contrib.auth.hashers import make_password 进行加密
            user_profile.password = make_password(pass_word)
            # 保存数据
            user_profile.save()

            # 注册之后写入欢迎注册，用个人中心的我的消息功能
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册xx教学在线网'

            # 发送邮件 从from utils.email_send import send_register_email
            send_register_email(user_name, 'register')
            # 注册成功返回login页面
            return render(request, 'login.html')
        else:
            # 注册失败返回register注册页面
            return render(request, 'register.html', {'register_form': register_form})

class LogoutView(View):
    '''退出的逻辑,在from django.contrib.auth import logout'''
    def get(self,request):
        logout(request)
        # django 2.0以下版本为from django.urls import reverse
        from django.urls import reverse
        # reverse()的作用是将URL的名称反向解析为redirect的访问地址
        return HttpResponseRedirect(reverse('index'))





# 登录业务逻辑，重写get和post
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        # 使用login_form去判断输入的用户名和密码是否符合loginform的要求
        if login_form.is_valid():
            # 如果用户名和密码是有效的，就继续以下的逻辑
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            # 如果从数据库中验证到有这个用户信息之后
            if user is not None:
                # 再判断用户是否激活，只有用户激活了才继续往下走
                if user.is_active:
                    # 当检查到用户是已经激活用户后，做login(request,)验证
                    login(request, user)  # 调取django里面django.contrib.auth import login的login函数做login验证
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活,请到注册邮箱激活'})
            else:
                # 如果没有输入的用户名或者密码错误，则返回错误提示
                return render(request, 'login.html', {'msg': '用户名或者密码错误'})
        else:
            # 如果用户验证失败的的就返回login_form里面的error信息，这个逻辑是从数据库验证数据之前就知道没有通过login_form的验证
            return render(request, 'login.html', {'login_form': login_form})


class IndexView(View):
    '''首页'''
    def get(self,request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        # 根据字段取出不是广告轮播的课程,和轮播的课程
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        all_orgs = CourseOrg.objects.all()[:15]

        return render(request,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'all_orgs':all_orgs,
        })


# 布置404，500页面，必须在项目的views写
def page_not_found(request,**kwargs):
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response

def page_error(request,**kwargs):
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response