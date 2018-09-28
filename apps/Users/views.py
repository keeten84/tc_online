from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from Users.forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from .models import *
# Create your views here.

#重新家载authenticate，是其可以检测用邮箱登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 忘记密码的业务逻辑
class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        # 实例话forgetform对象
        forget_form = ForgetForm(request.POST)
        # 如果通过Form检测
        if forget_form.is_valid():
            # 从前端获取用户的emial账号
            email = request.POST.get('email','')
            # 发送重置密码连接
            send_register_email(email,send_type='forget')
            # 发送完毕返回提示页面，提示用户发送成功
            return render(request,'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})



# 通过邮件激活用户的业务逻辑
class ActiveUserView(View):
    def get(self,request,active_code):
        # 从EmailVerifyRecode表中获取对象
        all_recodes = EmailVerifyRecord.objects.get(code=active_code)
        # 如果能够查找到对象，继续往下
        if all_recodes:
            # 从数据对象中遍历
            # for recode in all_recodes:
                # 从数据对象中获得email到数据
            email = all_recodes.email
            # 根据email数据在UserProfile中获取到用户资料
            user = UserProfile.objects.get(email = email)
            # 将激活字段从默认到False改为True
            user.is_active = True
            # 保存
            user.save()
        else:
            return render(request,'active_fail.html')
        # 激活之后跳转到登录页面
        return render(request,'login.html')


# 通过邮件激活用户的业务逻辑
class ResetView(View):
    def get(self,request,active_code):
        # 从EmailVerifyRecode表中获取对象
        all_recodes = EmailVerifyRecord.objects.get(code=active_code)
        # 如果能够查找到对象，继续往下
        if all_recodes:
            # 根据用户email进行查找
            email = all_recodes.email
            # 如果有就返回重置密码的页面
            return render(request,'password_reset.html',{'email':email})
        else:
            return render(request,'active_fail.html')
        # return render(request,'login.html')


# 修改密码的业务逻辑
class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':'密码不一致'})
            user = UserProfile.objects.get(email = email)
            user.password = make_password(pwd1)
            user.save()
            return render(request,'login.html')

        else:
            email = request.POST.get('email', '')
            return render(request,'password_reset.html',{'email':email,'modify_form':modify_form})





# 注册功能的业务逻辑
class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 从前端过去到用户名和密码
            user_name = request.POST.get('email', '')
            # 判断用户是否已经存在
            if UserProfile.objects.filter(email = user_name):
                # 如果用户已经存在，返回注册页面，并返回用户已经填写的数据和返回错误信息
                return render(request,'register.html',{'register_form':register_form,'msg':'用户已经被注册'})
            pass_word = request.POST.get('password', '')
            # 实例化UserProfile表
            user_profile = UserProfile()
            # 存储到表中
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False #设置用户未激活，必须通过点击发送邮件验证后才激活用户
            # 对密码加密后在保存到表中,使用from django.contrib.auth.hashers import make_password 进行加密
            user_profile.password = make_password(pass_word)
            # 保存数据
            user_profile.save()
            #发送邮件 从from utils.email_send import send_register_email
            send_register_email(user_name,'register')
            #注册成功返回login页面
            return render(request,'login.html')
        else:
            # 注册失败返回register注册页面
            return render(request,'register.html',{'register_form':register_form})


# 登录业务逻辑，重写get和post
class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{})
    def post(self,request):
        login_form = LoginForm(request.POST)
        # 使用login_form去判断输入的用户名和密码是否符合loginform的要求
        if login_form.is_valid():
            # 如果用户名和密码是有效的，就继续以下的逻辑
            user_name = request.POST.get('username','')
            pass_word = request.POST.get('password','')
            user = authenticate(username = user_name,password = pass_word)
            # 如果从数据库中验证到有这个用户信息之后
            if user is not None:
                # 再判断用户是否激活，只有用户激活了才继续往下走
                if user.is_active:
                    # 当检查到用户是已经激活用户后，做login(request,)验证
                    login(request,user) #调取django里面django.contrib.auth import login的login函数做login验证
                    return render(request,'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活,请到注册邮箱激活'})
            else:
                # 如果没有输入的用户名或者密码错误，则返回错误提示
                return render(request, 'login.html', {'msg': '用户名或者密码错误'})
        else:
            # 如果用户验证失败的的就返回login_form里面的error信息，这个逻辑是从数据库验证数据之前就知道没有通过login_form的验证
            return render(request,'login.html',{'login_form':login_form})

# 登录的业务逻辑(方法一，使用函数编写登录业务逻辑)
# def user_login(request):
#     if request.method == 'POST':
#         print('request.method == post')
#         user_name = request.POST.get('username','')
#         pass_word = request.POST.get('password','')
#         user = authenticate(username = user_name,password = pass_word)
#         if user is not None:
#             login(request,user)
#             return render(request,'index.html')
#         else:
#             # 登录错误的时候返回提示到前端页面
#             return render(request,'login.html',{'msg':'用户名或者密码错误'})
#
#     elif request.method == 'GET':
#         print('request.method = GET')
#         return render(request,'login.html',{})

