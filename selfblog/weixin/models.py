#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# ref:http://mp.weixin.qq.com/wiki/index.php?title=%E6%8E%A5%E6%94%B6%E6%99%AE%E9%80%9A%E6%B6%88%E6%81%AF

EVENT_ITEMS = (
    ('normal', '普通'),
    ('subscribe', '订阅'),
    ('unsubscribe', '退订'),
    ('client', 'CLICK'),
    ('view', 'VIEW'),
    ('scan', 'SCAN'),
)


class Menu(models.Model):
    """ 菜单
    """
    content = models.TextField()

    response_data = models.TextField(blank=True)

    success = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __unicode__(self):
        return self.content[:10]

    class Meta:
        verbose_name_plural = verbose_name = '菜单'


class ResponseMessage(models.Model):
    """ 根据事件要返回的消息设置
        
    如: 用户订阅后发送使用说明
    """
    event = models.CharField(max_length=50, choices=EVENT_ITEMS, verbose_name="事件")
    content = models.TextField()

    created_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    def __unicode__(self):
        return self.event

    class Meta:
        verbose_name_plural = verbose_name = '响应消息'


class Message(models.Model):
    """ 用户发过来的普通消息
    """
    to = models.CharField(max_length=100, verbose_name="接受者")
    from_user = models.CharField(max_length=100, verbose_name="发送者")
    msg_created_time = models.IntegerField(verbose_name="消息时间")
    msg_id = models.IntegerField(verbose_name="MsgId")

    body = models.TextField()
    response_content = models.TextField()

    created_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = '用户消息'


class Event(models.Model):
    """ 事件消息 """
    to = models.CharField(max_length=100, verbose_name="接受者")
    from_user = models.CharField(max_length=100, verbose_name="发送者")
    msg_created_time = models.IntegerField(verbose_name="消息时间")

    event = models.CharField(max_length=50, choices=EVENT_ITEMS, verbose_name="事件")
    body = models.TextField()

    created_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    def __unicode__(self):
        return self.event

    class Meta:
        verbose_name_plural = verbose_name = '接受到的事件'
