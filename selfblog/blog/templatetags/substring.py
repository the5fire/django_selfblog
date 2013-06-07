#coding:utf-8

from django import template

register = template.Library()


@register.filter(name='substring')
def substring(value, length):
    if not value:
        return u'无摘要'

    if len(value) > length:
        return '%s...' % value[:length]
    return value[:length]


@register.filter(name='sub')
def sub(value, param):
    if not value:
        return value
    try:
        value = int(value)
        param = int(param)
    except TypeError:
        return value
    return value - param
