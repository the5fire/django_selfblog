# coding: utf-8
from __future__ import absolute_import, unicode_literals

import xadmin
from xadmin import views


class GlobeSetting(object):
    site_title = 'the5fire博客后台'
    site_footer = 'power by the5fire'

xadmin.site.register(views.CommAdminView, GlobeSetting)
