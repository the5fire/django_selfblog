#coding:utf-8
from django.core.management.base import BaseCommand

from blog.models import Post


class Command(BaseCommand):
    args = 'no'
    help = 'import old post'

    def handle(self, *args, **options):
        format_all()


def format_all():
    posts = Post.objects.filter(is_old=True)

    for post in posts:
        print post.title 
        #处理代码
        post.content = post.content.replace("[cc lang=\'python\']", '<pre class="code literal-block">').replace("[/cc]", "</pre>")
        #处理换行
        post.content_html = post.content.replace('\n\n', '<br/>').replace('\n', '<br/>')
        post.save()
