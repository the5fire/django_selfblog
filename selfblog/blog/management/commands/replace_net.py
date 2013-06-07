#coding:utf-8
from django.core.management.base import BaseCommand

from blog.models import Post


class Command(BaseCommand):
    args = 'no'
    help = 'import old post'

    def handle(self, *args, **options):
        replace_all()


def replace_all():
    posts = Post.objects.filter(is_old=True)

    for post in posts:
        #print post.title 
        #处理代码
        index = post.content.find('the5fire.net')
        if index > 0:
            print post.title
            post.content = post.content.replace("www.the5fire.net", 'www.the5fire.com')
            post.content_html = post.content_html.replace("www.the5fire.net", 'www.the5fire.com')
            post.save()
