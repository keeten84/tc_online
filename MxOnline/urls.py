import xadmin,Users
from django.urls import include
from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.static import serve #处理静态文件的包
from MxOnline.settings import MEDIA_ROOT#导入media静态资源路径 STATIC_ROOT
from Users.views import LoginView, RegisterView, ActiveUserView,ForgetPwdView,\
    ResetView, ModifyPwdView, LogoutView,IndexView



urlpatterns = [
    url('admin/', xadmin.site.urls),
    # 主页映射
    # url('^$',TemplateView.as_view(template_name='index.html'),name='index'),
    # url('^login/$',TemplateView.as_view(template_name='login.html'),name='login')
    # url('^login/$',user_login,name='login') #基于函数的view方法
    url('^$',IndexView.as_view(),name='index'),
    #基于类的写法，登录业务逻辑的映射函数
    url('^login/$',LoginView.as_view(),name='login'),
    # 退出登录
    url('^logout/$',LogoutView.as_view(),name='logout'),
    # 注册业务逻辑的映射函数
    url('^register/$',RegisterView.as_view(),name='register'),
    #生成验证码的第三方库
    url(r'^captcha/', include('captcha.urls')),
    # 激活用户账号业务逻辑的映射函数
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name='user_active'),
    # 找回用户密码业务逻辑
    url(r'^forget/',ForgetPwdView.as_view(),name='forget_pwd'),
    # 处理账号重置密码连接的业务逻辑
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    # 处理修改密码的业务逻辑
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    # 配置上传资源文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT}),
    # 课程机构url配置映射的方法,url的分发
    url(r'^org/', include('organization.urls',namespace='org')),
    # 课程相关的url的映射
    url(r'^course/', include('course.urls',namespace='course')),
    # 个人中心的url映射分配
    url(r'^users/', include('Users.urls',namespace='users')),
    # 在生产环境下自己配置media访问函数
    # url(r'^static/(?P<path>.*)$', serve, {'document_root':STATIC_ROOT}),
]

# 全局404,500等页面配置方法(固定写法)，必须在项目的urls中设置
handler404 = 'Users.views.page_not_found'
handler500 = 'Users.views.page_error'
