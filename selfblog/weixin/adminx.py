#coding:utf-8
from __future__ import unicode_literals

import json
import urllib2

import requests
import xadmin
from django.conf import settings

from .models import Menu, ResponseMessage, Message, Event

weixin_menu = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s'
get_access_token = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (settings.WEIXIN_APPID, settings.WEIXIN_APPSECRET)  # noqa


class MenuAdmin(object):
    list_display = ('id', 'success', 'content', 'created_time')
    save_on_top = True
    access_token = None

    def save_model(self, request, obj, form, change):
        try:
            if self.set_menu(obj):
                obj.success = True
        except Exception as e:
            obj.response_data = str(e)
        obj.save()

    def set_menu(self, obj):
        # 调用微信设置菜单接口
        if not self.access_token:
            self.get_access_token()

        content = obj.content.encode('utf-8')
        f = requests.post(weixin_menu % self.access_token, data=content)
        data = json.loads(f.content)
        if data['errcode'] == 0:
            return True
        elif data['errcode'] == 42001:
            self.get_access_token()
            return self.set_menu(content)
        else:
            obj.response_data = data

    def get_access_token(self):
        content = urllib2.urlopen(get_access_token).read()
        data = json.loads(content)
        self.access_token = data['access_token']


xadmin.site.register(Menu, MenuAdmin)


class ResponseMessageAdmin(object):
    list_display = ('id', 'event', 'content', 'created_time')
    save_on_top = True

xadmin.site.register(ResponseMessage, ResponseMessageAdmin)


class MessageAdmin(object):
    list_display = ('id', 'to', 'from_user', 'msg_id', 'content', 'response_content', 'created_time')
    save_on_top = True

    def content(self, obj):
        data = json.loads(obj.body)
        return data['content']
    content.short_description = '内容'
    content.allow_tags = True


xadmin.site.register(Message, MessageAdmin)


class EventAdmin(object):
    list_display = ('id', 'to', 'from_user', 'event', 'body', 'created_time')
    save_on_top = True

xadmin.site.register(Event, EventAdmin)
