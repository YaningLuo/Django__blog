import re
import markdown
from django.shortcuts import render
from django.http import HttpResponse

from .models import Post
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin

# Create your views here.
# 这里我们不再是直接把字符串传给 HttpResponse 了，而是调用 django 提供的 render 函数。
# 这个函数根据我们传入的参数来构造 HttpResponse
# 我们首先吧http请求传了进去，让后render根据第二参数的值blog/index.html找到这个模板文件并读取模板中的内容
# 之后render根据我们传入的context参数的值吧模板中的变量替换成我们传递的变量的值{{title}}和{{welcome}}被替换成了context字典中对应的值
# 最终我们的html模板中的内容字符串被传递给httpResponse对象并返回浏览器（django在render函数里隐式地帮我们完成了这个过程

# def index(request):
#     """
#     主页视图函数中通过 Post.objects.all() 获取全部文章，而在归档和分类视图中，
#     我们不再使用 all 方法获取全部文章，而是使用 filter 来根据条件过滤
#     """
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})
#     # 这里我们使用 all() 方法从数据库里获取了全部的文章，存在了 post_list 变量里。
#     # all 方法返回的是一个 QuerySet（可以理解成一个类似于列表的数据结构），
#     # 由于通常来说博客文章列表是按文章发表时间倒序排列的，即最新的文章排在最前面，
#     # 所以我们紧接着调用了 order_by 方法对这个返回的 queryset 进行排序。
#     # 排序依据的字段是 created_time，即文章的创建时间。
#     # - 号表示逆序，如果不加 - 则是正序。
#     # 接着如之前所做，我们渲染了 blog\index.html 模板文件，并且把包含文章列表数据的 post_list 变量传给了模板


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     # 增加阅读量
#     post.increase_views()
#     md = markdown.Markdown(
#         extensions=[
#             'markdown.extensions.extra',  # 基础扩展
#             'markdown.extensions.codehilite',  # 语法高亮扩展
#             # 'markdown.extensions.toc',  # 生成目录扩展
#             # 需要引入ToxExtension和slugify
#             # extensions 中的 toc 拓展不再是字符串 markdown.extensions.toc ，
#             # 而是 TocExtension 的实例。TocExtension 在实例化时其 slugify 参数可以接受一个函数，
#             # 这个函数将被用于处理标题的锚点值。Markdown 内置的处理方法不能处理中文标题，
#             # 所以我们使用了 django.utils.text 中的 slugify 方法，该方法可以很好地处理中文
#
#             TocExtension(slugify=slugify),
#
#             # Markdown 在设置锚点时利用的是标题的值，由于通常我们的标题都是中文，Markdown 没法处理，
#             # 所以它就忽略的标题的值，而是简单地在后面加了个 _1 这样的锚点值。
#             # 为了解决这一个问题，需要修改一下传给 extentions 的参数
#             # 和之前不同的是，extensions 中的 toc 拓展不再是字符串 markdown.extensions.toc ，
#             # 而是 TocExtension 的实例。TocExtension 在实例化时其 slugify 参数可以接受一个函数，
#             # 这个函数将被用于处理标题的锚点值。Markdown 内置的处理方法不能处g理中文标题，
#             # 所以我们使用了 django.utils.text 中的 slugify 方法，该方法可以很好地处理中文
#         ]
#     )
#     # 和之前的代码不同，我们没有直接用 markdown.markdown() 方法来渲染 post.body 中的内容，
#     # 而是先实例化了一个 markdown.Markdown 对象 md，和 markdown.markdown() 方法一样，
#     # 也传入了 extensions 参数。接着我们便使用该实例的 convert 方法将 post.body 中的 Markdown 文本解析成 HTML 文本。
#     # 而一旦调用该方法后，实例 md 就会多出一个 toc 属性，这个属性的值就是内容的目录，
#     # 我们把 md.toc 的值赋给 post.toc 属性（要注意这个 post 实例本身是没有 toc 属性的，我们给它动态添加了 toc 属性，这就是 Python 动态语言的好处）
#     """正则匹配目录是否存在"""
#     post.body = md.convert(post.body)
#     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#     post.toc = m.group(1) if m is not None else ''
#     # 这里我们正则表达式去匹配生成的目录中包裹在 ul 标签中的内容，
#     # 如果不为空，说明目录，就把 ul 标签中的值提取出来（目的是只要包含目录内容的最核心部分，多余的 HTML 标签结构丢掉）赋值给 post.toc；
#     # 否则，将 post 的 toc 置为空字符串，然后我们就可以在模板中通过判断 post.toc 是否为空
#
#     # post.body = md.convert(post.body)
#     # post.toc = md.toc
#
#     # 这样我们在模板中显示{{post.body}}的时候，就不再是原始的Markdown文本了，
#     # 而是解析过后的HTML文本。注意这里我们给markdown解析函数传递了额外的参数extensions，
#     # 它是对Markdown语法的拓展，这里使用了三个拓展，分别是xtra、codehilite、toc。extra本身包含很多基础拓展，
#     # 而codehilite是语法高亮拓展，这为后面的实现代码高亮功能提供基础，而toc则允许自动生成目录
#     # markdown.markdown()方法把post.bod中的Markdown文本解析成了HTML文本。同时我们还给该方法提供了一个extensions的额外参数。其中
#     # markdown.extensions.toc就是自动生成目录的拓展（这里可以看出我们有先见之明，如果你之前没有添加的话记得现在添加进去）
#     # 在渲染 Markdown 文本时加入了 toc 拓展后，就可以在文中插入目录了。方法是在书写 Markdown 文本时，在你想生成目录的地方插入`[TOC] 标记即可
#     return render(request, 'blog/detail.html', context={'post': post})
#
#     # 视图函数很简单，它根据我们从 URL 捕获的文章 id（也就是 pk，这里 pk 和 id 是等价的）获取数据库中文章 id 为该值的记录，
#     # 然后传递给模板。注意这里我们用到了从 django.shortcuts 模块导入的 get_object_or_404 方法，
#     # 其作用就是当传入的 pk 对应的 Post 在数据库存在时，就返回对应的 post，如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在


# def index(request):
#     """
#     主页视图函数中通过 Post.objects.all() 获取全部文章，而在归档和分类视图中，
#     我们不再使用 all 方法获取全部文章，而是使用 filter 来根据条件过滤
#     """
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})


def archive(request, year, month):
    post_list = Post.objects.filter(
        created_time__year=year,
        created_time__month=month,
    ).order_by('-created_time')


# 这里使用了模型管理器（objects）的 filter 方法来过滤文章。
# 由于是按照日期归档，因此这里根据文章发表的年和月来过滤。
# 具体来说，就是根据 created_time 的 year 和 month 属性过滤，筛选出文章发表在对应的 year 年和 month 月的文章。
# 注意这里 created_time 是 Python 的 date 对象，其有一个 year 和 month 属性，
# 我们在 页面侧边栏：使用自定义模板标签 使用过这个属性。Python 中调用属性的方式通常是 created_time.year，
# 但是由于这里作为方法的参数列表，所以 django 要求我们把点替换成了两个下划线，即 created_time__year。
# 同时和 index 视图中一样，我们对返回的文章列表进行了排序。此外由于归档页面和首页展示文章的形式是一样的，
# 因此直接复用了 index.html 模板
# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     # return render(request, 'blog/index.html', context={'post_list': post_list})
#     return render(request, 'blog/index.html', context={'post_list': post_list})
#     # 这里我们首先根据传入的 pk 值（也就是被访问的分类的 id 值）从数据库中获取到这个分类。get_object_or_404 函数和 detail 视图中一样，
#     # 其作用是如果用户访问的分类不存在，则返回一个 404 错误页面以提示用户访问的资源不存在。
#     # 然后我们通过模型管理器的 filter 方法过滤出了该分类下的全部文章。同样也和首页视图中一样对返回的文章列表进行了排序


def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    content_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 5
    # 要写一个视图首先要继承django提供的某个类视图,至于继承那个视图,需要根据视图功能而定
    # 例如这里的IndexView的功能是那个数据库中获取文章(post)列表,ListView就是从数据库中获取某个模型列表数据的,所以IndexView继承ListView
    # 然后就是通过一些属性来指定这个视图函数需要做的事情,这里我们指定三个属性
    # model: 将model指定为post,告诉django我要获取数据模型是post
    # template_name: 指定这个视图渲染的模板
    # context_object_name: 指定获取的模板列表数据保存的变量名,这个变量会被传递给模板
    # 我们与index视图函数对比一下
    # index首先通过Post.object.all()从数据库中获取文章(post)列表数据吗,并保存到post_list变量中.
    # 在类视图中这个过程ListView已经帮我们做了,我们只需要告诉ListView去数据库中获取的模型是Post,而不是Comment或者其它什么模型,即指定model=post
    # 将获得的模型数据列表保存到post_list里,即指定context_object_name='post_list'
    # 然后渲染blog/index.html模板文件,index视图函数中使用render函数,但这个过程ListView已经帮我们做了,我们只需要指定那个模板即可


class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
        # 和 IndexView 不同的地方是，我们覆写了父类的 get_queryset 方法。
        # 该方法默认获取指定模型的全部列表数据。为了获取指定分类下的文章列表数据，我们覆写该方法，改变它的默认行为。
        # 首先是需要根据从 URL 中捕获的分类 id（也就是 pk）获取分类，
        # 这和 category 视图函数中的过程是一样的。
        # 不过注意一点的是，在类视图中，从 URL 捕获的路径参数值保存在实例的 kwargs 属性（是一个字典）里，非路径参数值保存在实例的 args 属性（是一个列表）里。
        # 所以我们使了 self.kwargs.get('pk') 来获取从 URL 捕获的分类 id 值。
        # 然后我们调用父类的 get_queryset 方法获得全部文章列表，
        # 紧接着就对返回的结果调用了 filter 方法来筛选该分类下的全部文章并返回。


class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    # def get_object(self, queryset=None):
    #     # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
    #     post = super().get_object(queryset=None)
    #     md = markdown.Markdown(extensions=[
    #         'markdown.extensions.extra',
    #         'markdown.extensions.codehilite',
    #         # 记得在顶部引入 TocExtension 和 slugify
    #         TocExtension(slugify=slugify),
    #     ])
    #     post.body = md.convert(post.body)

    #     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    #     post.toc = m.group(1) if m is not None else ''

    #     return post
    # PostDetailView 稍微复杂一点，主要是等价的 detail 视图函数本来就比较复杂，下面来一步步对照 detail 视图函数中的代码讲解。
    # 首先我们为 PostDetailView 类指定了一些属性的值，这些属性的含义和 ListView 中是一样的，这里不再重复讲解。
    # 紧接着我们覆写了 get 方法。这对应着 detail 视图函数中将 post 的阅读量 +1 的那部分代码。事实上，你可以简单地把 get 方法的调用看成是 detail 视图函数的调用。
    # 接着我们又复写了 get_object 方法。这对应着 detail 视图函数中根据文章的 id（也就是 pk）获取文章，然后对文章的 post.body 进行 Markdown 解析的代码部分。
    # 你也许会被这么多方法搞乱，为了便于理解，你可以简单地把 get 方法看成是 detail 视图函数，至于其它的像 get_object、get_context_data 都是辅助方法，
    # 这些方法最终在 get 方法中被调用，这里你没有看到被调用的原因是它们隐含在了 super(PostDetailView, self).get(request, *args, **kwargs) 即父类 get 方法的调用中。
    # 最终传递给浏览器的 HTTP 响应就是 get 方法返回的 HttpResponse 对象。
