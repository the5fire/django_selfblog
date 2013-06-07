#coding:utf-8

from django.contrib.sitemaps import Sitemap

from blog.models import Post

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.2

    def items(self):
        return Post.objects.filter(status=0)

    def lastmod(self, obj):
        return obj.create_time

    def location(self, obj):
        return '/%s.html' % obj.alias
