#!/usr/bin/python

# 编写者:沫
# 时间:07:18 下午
from django.contrib.syndication.views import Feed
from .models import Post


class AllPostsRssFeed(Feed):
    # 显示在聚合阅读上的标题
    title = "你好,摸鱼崽"

    # 通过聚合阅读器跳转到网站的地址
    link = "/"

    # 显示在聚合阅读器上的描述信息
    description = "一起来摸鱼呀!"

    # 需要显示的内容条目
    def items(self):
        return Post.objects.all()

    # 聚合中显示的内容条目标题
    def item_title(self, item):
        return "[%s] %s" % (item.category, item.title)

    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.body_html
    # item 是文章 （Post 模型的实例），聚合内容的描述我们返回了 body_html 属性的值。模型中原本使用 body 属性存储博客文章的内容，
    # 但是这些内容是以 Markdown 格式的，并非所有的聚合内容阅读器都支持 Markdown 格式的解析，因此我们返回的是已经解析后的 HTML 格式内容
