#coding:utf-8
import re
from datetime import datetime
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from blog.models import Post, Category


class Command(BaseCommand):
    args = 'no'
    help = 'import old post'

    def handle(self, *args, **options):
        parse_xml()


def parse_xml():
    et = ET.ElementTree(file='/home/the5fire/Downloads/the5fire.xml')
    root = et.getroot()
    user = User.objects.get(username='the5fire')
    count = 1
    alias_re = re.compile(r'^[a-z|0-9|\-]+$')

    for channel in root.findall('channel'):
        for item in channel.findall('item'):
            title = item.find('title')
            post_name = item.find('{http://wordpress.org/export/1.2/}post_name')
            pubDate = item.find('pubDate')
            description = item.find('description')
            content = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
            categories = item.findall('category')
            tags = []
            category = Category()
            for ca in categories:
                if ca.attrib['domain'] == 'post_tag':
                    tags.append(ca.text)
                else:
                    try:
                        category = Category.objects.get(name=ca.text)
                    except Category.DoesNotExist:
                        category.name = ca.text
                        if alias_re.match(ca.attrib['nicename']):
                            category.alias = ca.attrib['nicename']
                        else:
                            category.alias = category.name
                        print category.alias
                        category.save()
            try:
                Post.objects.get(title=title.text)
                print title.text, 'already exist'
                continue
            except Post.DoesNotExist:
                pass 

            post = Post()
            post.title = title.text
            post.category = category 
            if alias_re.match(post_name.text):
                post.alias = post_name.text
            else:
                post.alias = title.text 
            print post.alias
            post.content = content.text
            post.content_html = content.text
            if not description.text:
                post.summary = content.text[:140]
            else:
                post.summary = description.text
            post.is_old = True
            post.tags = ','.join(tags)
            create_time = pubDate.text[:-6]
            tf = '%a, %d %b %Y %H:%M:%S'
            post.old_pub_time = datetime.strptime(create_time, tf)
            print post.old_pub_time
            post.author = user 
            try:
                post.save()
                print count, post
                count += 1
            except Exception, e:
                print e

