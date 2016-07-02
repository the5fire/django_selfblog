# coding:utf-8

from .base import *  # noqa

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DOMAIN = 'http://localhost:8000'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'selfblog.sqlite3',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar', )
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware', )
