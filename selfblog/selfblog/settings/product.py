# coding:utf-8

from .base import * # noqa

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DOMAIN = 'http://www.the5fire.com'   # yourdomain
DB_NAME = 'mydb'
DB_USER = 'the5fire'
DB_PWD = 'the5fire'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'the5fire',
        'PASSWORD': 'the5fire',
        'HOST': '',
        'PORT': '',
    }
}
