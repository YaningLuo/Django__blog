#!/usr/bin/python

# 编写者:沫
# 时间:07:09 下午
from django import template
from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
    }
# show_comment_form 模板标签使用时会接受一个 post（文章 Post 模型的实例）作为参数，
# 同时也可能传入一个评论表单 CommentForm 的实例 form，如果没有接受到评论表单参数，
# 模板标签就会新创建一个 CommentForm 的实例（一个没有绑定任何数据的空表单）传给模板，
# 否则就直接将接受到的评论表单实例直接传给模板，这主要是为了复用已有的评论表单实例


@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    comment_list = post.comment_set.all().order_by('-created_time')
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }
    # 我们使用了 post.comment_set.all() 来获取 post 对应的全部评论。
    # Comment 和Post 是通过 ForeignKey 关联的，回顾一下我们当初获取某个分类 cate 下的全部文章时的代码：Post.objects.filter(category=cate)。
    # 这里 post.comment_set.all() 也等价于 Comment.objects.filter(post=post)，即根据 post 来过滤该 post 下的全部评论。
    # 但既然我们已经有了一个 Post 模型的实例 post（它对应的是 Post 在数据库中的一条记录），那么获取和 post 关联的评论列表有一个简单方法，
    # 即调用它的 xxx_set 属性来获取一个类似于 objects 的模型管理器，然后调用其 all 方法来返回这个 post 关联的全部评论。
    # 其中 xxx_set 中的 xxx 为关联模型的类名（小写）。例如 Post.objects.filter(category=cate) 也可以等价写为 cate.post_set.all()
