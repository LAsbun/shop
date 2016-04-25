"""
Django settings for shop project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#path helper
locate = lambda x:os.path.join(
    os.path.dirname(os.path.abspath(__file__)),x
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$g_#m5zx#^l6+4fp=2v6qn5yzgcno21t4^9q61!0*#u=^@0j(t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1:8010']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third
    'widget_tweaks',
    'treebeard',
    # myapp
    'customer',
    'category',
    'basket',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shop4',
        'USER':'root',
        'PASSWORD':'aaaaa'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh_cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# Media root
STATIC_ROOT = locate('../public/static')

# static file dirs
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    # '/home/sws/onlineshop/shop/images'
)

# static files finder
STATICFILES_FINDERS=(
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

#Media_url
MEDIA_URL = 'uploads/'

MEDIA_ROOT = os.path.join(BASE_DIR,'images/upload/')


# # log root
# LOG_ROOT = locate('log')
#
# LOGGING = {
#     'version' : 1,
#     'disable_existing_logger':True,
#     'formatters':{
#         'verbose':{
#             'format':'%(levelname)s %s(asctime)s %(module)s %(message)s',
#         },
#         'simple':{
#             'format':'[%(asctime)s] %(message)s'
#         },
#     }
#     'filters':{
#         'require_debug-false'
#     }
# }


# DEFAULT LOGIN URL
# LOGIN_REDIRECT_URL =

# File && image
IMAGE_UPLOAD_FOLDER = 'images'