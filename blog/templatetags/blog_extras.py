#!/usr/bin/python

# 编写者:沫
# 时间:09:23 上午
from django import template
from ..models import Post, Category, Tag
from django.db.models.aggregates import Count
from blog.models import Category

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    """最新文章模板"""
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }
    # 我们导入template模块，然后实例化了一个template。Library类
    # 并将函数show_recent_posts装饰为register.inclusion_tag，这样就告诉django，这个函数是我们自己定义一个类型为inclusion_tag的模板标签
    # inclusion_tag 模板标签和视图函数的功能类似，
    # 它返回一个字典值，字典中的值将作为模板变量，传入由 inclusion_tag 装饰器第一个参数指定的模板。
    # 当我们在模板中通过 {% show_recent_posts %}使用自己定义的模板标签时，django 会将指定模板的内容使用模板标签返回的模板变量渲染后替换
    # inclusion_tag 装饰器的参数 takes_context 设置为 True 时将告诉 django，
    # 在渲染 _recent_posts.html 模板时，不仅传入show_recent_posts 返回的模板变量，
    # 同时会传入父模板（即使用 {% show_recent_posts %} 模板标签的模板）上下文（可以简单理解为渲染父模板的视图函数传入父模板的模板变量以及 django 自己传入的模板变量）。
    # 当然这里并没有用到这个上下文，这里只是做个简单演示，如果需要用到，就可以在模板标签函数的定义中使用 context 变量引用这个上下文
    # 接下来就是定义模板 _recent_posts.html 的内容。在 templates\blogs 目录下创建一个 inclusions 文件夹，然后创建一个 _recent_posts.html 文件


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    """归档模板"""
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }
    # Post.objects.dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间（已去重），
    # 且是 Python 的 date 对象，精确到月份，降序排列。
    # 接受的三个参数值表明了这些含义，一个是 created_time ，
    # 即 Post 的创建时间，month 是精度，order='DESC' 表明降序排列（即离当前越近的时间越排在前面）
    # 例如我们写了 3 篇文章，分别发布于 2017 年 2 月 21 日、2017 年 3 月 25 日、2017 年 3 月 28 日，
    # 那么 dates 函数将返回 2017 年 3 月 和 2017 年 2 月这样一个时间列表，且降序排列，从而帮助我们实现按月归档的目的


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    """分类模板"""
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
        # 'category_list': Category.objects.all(),  # 分类模板标签函数中使用到了 Category 类，其定义在 blog.models.py 文件中，使用前记得先导入它
    }
# 这个 Category.objects.annotate 方法和 Category.objects.all 有点类似，
# 它会返回数据库中全部 Category 的记录，但同时它还会做一些额外的事情，在这里我们希望它做的额外事情就是去统计返回的 Category 记录的集合中每条记录下的文章数。
# 代码中的 Count 方法为我们做了这个事，它接收一个和 Categoty 相关联的模型参数名（这里是 Post，通过 ForeignKey 关联的），
# 然后它便会统计 Category 记录的集合中每条记录下的与之关联的 Post 记录的行数，也就是文章数，最后把这个值保存到 num_posts 属性中。
# 此外，我们还对结果集做了一个过滤，使用 filter 方法把 num_posts 的值小于 1 的分类过滤掉。因为 num_posts 的值小于 1 表示该分类下没有文章，
# 没有文章的分类我们不希望它在页面中显示。关于 filter 函数以及查询表达式（双下划线）在之前已经讲过


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    """标签云模板"""
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
        # 'tag_list': Tag.objects.all(),
    }

# 此前侧边栏中各个功能块都替换成了模板标签，其实实际内容还是一样的，只是我们将其挪到了模块化的模板中，并有这些自定义的模板标签负责渲染这些内容
# 此外我们定义的 show_recent_posts 标签可以接收参数，默认为 5，即显示 5 篇文章，
# 如果要控制其显示 10 篇文章，可以使用 {% show_recent_posts 10 %} 这种方式传入参数

# 如果你按照教程的步骤做完后发现报错，请按以下顺序检查。
# 检查目录结构是否正确。确保 templatetags 位于 blog 目录下，且目录名必须为 templatetags。具体请对照上文给出的目录结构。
# 确保 templatetags 目录下有 __init__.py 文件。
# 确保通过 register = template.Library() 和 @register.inclusion_tag 装饰器将函数装饰为一个模板标签。
# 确保在使用模板标签以前导入了 blog_extras，即 {% load blog_extras%}。注意要在使用任何 blog_extras下的模板标签以前导入它。
# 确保模板标签的语法使用正确，即 {% load blog_extras %}，注意 { 和 % 以及 % 和 } 之间没有任何空格
