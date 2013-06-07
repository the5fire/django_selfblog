#coding:utf-8
import logging
import md5
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from time import time
from django.core.cache import get_cache

logger = logging.getLogger(__name__)

try:
    cache = get_cache('memcache')
except ImportError as e:
    logger.warn(u'加载memcache时出错:[%s], 改为内存缓存', e)
    cache = get_cache('default')


def cache_decorator(expiration=3*60):

    def wrapper(func):
        def news(*args, **kwargs):
            unique_str = repr((func, args, kwargs))
            m = md5.new(unique_str)
            key = m.hexdigest()
            value = cache.get(key)
            if value:
                return value
            else:
                value = func(*args, **kwargs)
                cache.set(key, value, expiration)
                return value
        return news
    return wrapper


#copy from https://github.com/the5fire/Python-LRU-cache
class LRUCacheDict(object):
    def __init__(self, max_size=1024, expiration=15*60):
        self.max_size = max_size
        self.expiration = expiration

        self.__values = {}
        self.__expire_times = OrderedDict()
        self.__access_times = OrderedDict()

    def items(self):
        return self.__values.items()

    def values(self):
        return self.__values.values()

    def size(self):
        return len(self.__values)

    def clear(self):
        self.__values.clear()
        self.__expire_times.clear()
        self.__access_times.clear()

    def has_key(self, key):
        return key in self.__values

    def __setitem__(self, key, value):
        t = int(time())
        self.__delete__(key)
        self.__values[key] = value
        self.__access_times[key] = t
        self.__expire_times[key] = t + self.expiration
        self.cleanup()

    def __getitem__(self, key):
        t = int(time())
        del self.__access_times[key]
        self.__access_times[key] = t
        self.cleanup()
        return self.__values[key]

    def __delete__(self, key):
        if self.__values.has_key(key):
            del self.__values[key]
            del self.__expire_times[key]
            del self.__access_times[key]

    def cleanup(self):
        if self.expiration is None:
            return None
        t = int(time())
        #Delete expired
        for k in self.__expire_times.iterkeys():
            if self.__expire_times[k] < t:
                self.__delete__(k)
            else:
                break

        #If we have more than self.max_size items, delete the oldest
        while (len(self.__values) > self.max_size):
            for k in self.__access_times.iterkeys():
                self.__delete__(k)
                break
