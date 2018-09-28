from django.urls import include
import xadmin
from django.conf.urls import url
from django.views.generic import TemplateView
from Users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from organization.views import OrgView
from django.views.static import serve #处理静态文件的包
from MxOnline.settings import MEDIA_ROOT #导入media静态资源路径

urlpatterns = [
    url('admin/', xadmin.site.urls),
    # 主页映射
    url('^$',TemplateView.as_view(template_name='index.html'),name='index'),
    # url('^login/$',TemplateView.as_view(template_name='login.html'),name='login')
    # url('^login/$',user_login,name='login') #基于函数的view方法

    #基于类的写法，登录业务逻辑的映射函数
    url('^login/$',LoginView.as_view(),name='login'),
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

]
