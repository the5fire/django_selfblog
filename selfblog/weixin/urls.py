#coding:utf-8
from django.conf.urls import patterns, url

from .views import interface

urlpatterns = patterns(
    '',
    url(r'interface/$', interface, name='interface'),
)
