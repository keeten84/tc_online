"""
Django settings for MxOnline project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 搜索目录到配置：如果所有app都放在一个apps下的话，需要添加下列语句，将apps放到搜索路径中
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
#为xadmin添加搜索路径
sys.path.insert(0,os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i+j&(wf935kqot8#-pk&gul&kt@c#wpz7yhc4^=8@_o9+ywg+p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
#重载检测用户名的方法
AUTHENTICATION_BACKENDS = (
    'Users.views.CustomBackend',
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Users',
    'course',
    'operation',
    'organization',
    'xadmin',            #以下两步去注册xadmin： 注册xadmin和 crispy-forms
    'crispy_forms',
    'captcha', #验证码的第三方库
    'pure_pagination', #快速分页的第三方库
    'DjangoUeditor',
]

# 当自定义userprofile（继承自django内部user表）覆盖默认user表的时候，需要添加以下代码去重载user表
AUTH_USER_MODEL = 'Users.UserProfile'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MxOnline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 配置解析{{MEDIA_URL}}的方法, django 2.0之前版本配置为django.template.context_processors.media
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'MxOnline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mxonline',
        'USER':'root',
        'PASSWORD':'andy1984',
        'HOST':'127.0.0.1'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans' #zh-hans en-us

TIME_ZONE = 'Asia/Shanghai' #Asia/Shanghai

USE_I18N = True

USE_L10N = True

USE_TZ = False #这里如果用本地时间，必须改为false，否则用UTC时间


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'/static/'),
)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 配置发送email邮件服务器
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'projectemail84@163.com'
EMAIL_HOST_PASSWORD = 'admin1234'
EMAIL_FROM = 'projectemail84@163.com'

# 配置资源文件的配置方法
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# STATIC_ROOT = os.path.join(BASE_DIR,'static')

