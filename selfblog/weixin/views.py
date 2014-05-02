#coding:utf-8
from __future__ import unicode_literals

import logging
import time
import json
import hashlib
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Message, ResponseMessage, Event

TOKEN = 'your token'

logger = logging.getLogger(__name__)


@csrf_exempt
def interface(request):
    if not request.GET and not request.body:
        return HttpResponse()

    status, result = check_sign(request)
    if request.method == 'GET':
        return HttpResponse(result)
    else:
        if status:
            return dispatch_event(request)
        else:
            logger.warning('sign fail!', **request.GET)
            return HttpResponse('')


def check_sign(request):
    """ 认证接口

    加密/校验流程如下：
    1. 将token、timestamp、nonce三个参数进行字典序排序
    2. 将三个参数字符串拼接成一个字符串进行sha1加密
    3. 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    """
    signature = request.GET.get('signature')

    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echostr = request.GET.get('echostr')

    source = ''.join(sorted([timestamp, nonce, TOKEN]))
    sign = hashlib.sha1(source).hexdigest()

    status = False
    result = ''
    if sign == signature:
        status = True
        result = echostr

    return status, result


def dispatch_event(request):
    """ 事件分发函数，根据post数据中的event
    """
    xml = request.body
    root = ET.fromstring(xml)
    params = {elem.tag.lower(): elem.text for elem in root}

    try:
        handler_name = '%s_handler' % params['event'].lower()
        handler = globals()[handler_name]
    except KeyError:
        handler = default_handler

    result = handler(params)

    if not result:
        return HttpResponse('')

    user_extend = {
        'ToUserName': params['fromusername'],
        'FromUserName': params['tousername'],
        'CreateTime': int(time.time()),
    }
    result.update(user_extend)
    # 组合为xml
    content = build_xml(result)
    return HttpResponse(content)


def default_handler(params):
    """ 非Event接口，回应用户发来的消息 """
    event_type = 'normal'
    return_content = None
    try:
        content = params['content']
    except KeyError:
        logger.error('[weixin] default_handler error', **params)
    else:
        # 获取操作类型：搜索 python招聘
        if ' ' in content:
            operate, content = content.split(' ', 1)
        else:
            operate = ''

        if operate in ('搜索', 'search'):
            return_content = '未搜索到相关内容'

    if not return_content:
        rm = ResponseMessage.objects.filter(event=event_type).latest('id')
        return_content = rm.content

    result = {
        'MsgType': 'text',
        'Content': return_content,
    }

    message = Message()
    message.to = params['tousername']
    message.from_user = params['fromusername']
    message.msg_created_time = int(params['createtime'])
    message.msg_id = int(params['msgid'])
    message.body = json.dumps(params)

    message.response_content = return_content
    message.save()

    return result


def subscribe_handler(params):
    """ 处理订阅事件 """
    event_type = 'subscribe'
    save_event(params, event_type)

    rm = ResponseMessage.objects.filter(event=event_type).latest('id')
    result = {
        'MsgType': 'text',
        'Content': rm.content
    }
    return result


def unsubscribe_handler(params):
    event_type = 'unsubscribe'
    save_event(params, event_type)


def scan_hanlder(params):
    """ 用户已关注时的事件推送 """
    event_type = 'unsubscribe'
    save_event(params, event_type)


def save_event(params, event_type):
    event = Event()
    event.event = event_type
    event.to = params['tousername']
    event.from_user = params['fromusername']
    event.msg_created_time = int(params['createtime'])
    event.body = json.dumps(params)
    event.save()


def click_handler(params):
    """ 点击菜单拉取消息时的事件推送 """
    event_type = 'click'
    save_event(params, event_type)
    # TODO: 需要进一步处理


def view_handler(params):
    """ 点击菜单跳转链接时的事件推送 """
    event_type = 'view'
    save_event(params, event_type)
    # TODO: 需要进一步处理


def build_xml(data):
    sequence = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (str, unicode)):
                sequence.append("<%(key)s><![CDATA[%(value)s]]></%(key)s>" % locals())
            elif isinstance(value, (list, dict)):
                value = build_xml(value)
                sequence.append("<%(key)s>%(value)s</%(key)s>" % locals())
            else:
                sequence.append("<%(key)s>%(value)s</%(key)s>" % locals())

    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (list, dict)):
                sequence.append("<item>%s</item>" % build_xml(item))
            elif isinstance(value, (str, unicode)):
                sequence.append("<item><![CDATA[%s]]></item>" % item)
            else:
                sequence.append("<item>%s</item>" % item)
    body = "".join(sequence)
    return '<xml>%s</xml>' % body
