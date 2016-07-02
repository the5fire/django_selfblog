# coding:utf-8
import os
from os import path

ROOT_PATH = path.abspath(path.join(path.dirname('settings.py'), path.pardir))

ADMINS = (
    ('the5fire', 'thefivefire@gmail.com'),
)
ALLOWED_HOSTS = ['localhost', '.the5fire.com']

MANAGERS = ADMINS
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-cn'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = ''
MEDIA_URL = '/media/'
# STATIC_ROOT = ''
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    path.join(ROOT_PATH, 'selfblog/static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'm_t&=vit))7cic$zfdl^7wfsc+$e1@_p=4@bmc54pp%25n#*%1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pingback.middleware.PingbackMiddleware',
    'blog.middleware.OnlineMiddleware',
)
INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'selfblog.urls'
WSGI_APPLICATION = 'selfblog.wsgi.application'

TEMPLATE_DIRS = (
    path.join(ROOT_PATH, 'blog/templates'),
)

DIRECTORY_URLS = (
    'http://ping.blogs.yandex.ru/RPC2',
    'http://rpc.technorati.com/rpc/ping',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_xmlrpc',

    'xadmin',
    'crispy_forms',
    'pingback',
    'duoshuo',

    'blog',
    'weixin',
)


LOG_PATH = os.path.join(ROOT_PATH, '..', '..')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] %(module)s : %(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s] [%(levelname)s] %(module)s : %(message)s'
        }
    },

    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_PATH, 'info.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 10,
            'mode': 'a',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        }
    },
    'loggers': {
        '': {
            'handlers': ['file_info', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['file_info', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'options': {
            'MAX_ENTRIES': 1024,
        }
    },
    'memcache': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/home/the5fire/memcached.sock',
        'options': {
            'MAX_ENTRIES': 1024,
        }
    },
}


# 配置文章开头使用rst格式无显示的问题
RESTRUCTUREDTEXT_FILTER_SETTINGS = {
    'doctitle_xform': False,
}

PAGE_NUM = 10
RECENTLY_NUM = 15
HOT_NUM = 15
ONE_DAY = 24*60*60
FIF_MIN = 15 * 60
FIVE_MIN = 5 * 60

DUOSHUO_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
DUOSHUO_SHORT_NAME = 'xxxxxxxx'

# 微信
WEIXIN_APPID = 0
WEIXIN_APPSECRET = ''
