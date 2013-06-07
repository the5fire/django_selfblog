#coding:utf-8
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from blog.models import Post


class ExtendedRSSFeed(Rss201rev2Feed):
    mime_type = 'application/xml'
    """
    Create a type of RSS feed that has content:encoded elements.
    """
    def root_attributes(self):
        attrs = super(ExtendedRSSFeed, self).root_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        return attrs

    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement(u'content:encoded', item['content_encoded'])


class LatestEntriesFeed(Feed):
    feed_type = ExtendedRSSFeed

    # Elements for the top-level, channel.
    title = u"the5fire的技术博客"
    link = "http://www.the5fire.com"
    author = 'the5fire'
    description = u"关注python、vim、linux、web开发和互联网--life is short, we need python."

    def items(self):
        return Post.objects.filter(status=0).order_by('-create_time')[:10]

    def item_extra_kwargs(self, item):
        return {'content_encoded': self.item_content_encoded(item)}

    # Elements for each item.
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content_html

    def item_author_name(self, item):
        if (item.author.get_full_name()):
            return item.author.get_full_name()
        else:
            return item.author

    def item_pubdate(self, item):
        return item.create_time

    def item_content_encoded(self, item):
        return item.content_html
