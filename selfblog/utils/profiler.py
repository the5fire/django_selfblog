#coding:utf-8
from django.db import connection
from pprint import pprint as pp
import time


def print_queries(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print 'the function[%s] cast you [%s]s' % (func.__name__, (time.time() - start))
        pp(connection.queries)
        return result
    return wrapper
