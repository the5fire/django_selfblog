#coding:utf-8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page

import xadmin
xadmin.autodiscover()

from blog.views import (IndexView, CategoryListView, TagsListView,
                        PostDetailView, PageDetailView)
from feeds import LatestEntriesFeed
from sitemap import PostSitemap

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='home'),

    url(r'^feed|rss/$', LatestEntriesFeed()),
    url(r'^sitemap\.xml$', cache_page(60 * 60 * 12)(sitemap_views.sitemap), {'sitemaps': {'posts': PostSitemap}}),

    url(r'^category/(?P<alias>\w+)/', CategoryListView.as_view()),
    url(r'^tag/(?P<tag>[\w|\.|\-]+)/$', TagsListView.as_view()),

    url(r'^xadmin/', include(xadmin.site.urls), name='xadmin'),

    url(r'^xmlrpc/$', 'django_xmlrpc.views.handle_xmlrpc', {}, 'xmlrpc'),

    #放到最后
    url(r'^(?P<slug>[\w|\-|\d|\W]+?).html$', PostDetailView.as_view()),
    url(r'^(?P<slug>\w+)/$', PageDetailView.as_view()),
)

urlpatterns += staticfiles_urlpatterns()
