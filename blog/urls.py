#!/usr/bin/python

"""
编写者:沫
时间:08:45 下午
"""
from django.urls import path
from . import views

# django 的做法是把不同的网址对应的处理函数写在一个 urls.py 文件里，当用户访问某个网址时，django 就去会这个文件里找
# 如果找到这个网址，就会调用和它绑定在一起的处理函数（叫做视图函数）
# 我们首先从 django.urls 导入了 path 函数，又从当前目录下导入了 views 模块。
# 然后我们把网址和处理函数的关系写在了 urlpatterns 列表里
# 绑定关系的写法是把网址和对应的处理函数作为参数传给 path 函数（第一个参数是网址，第二个参数是处理函数）
# 另外我们还传递了另外一个参数 name，这个参数的值将作为处理函数 index 的别名，这在以后会用到

# 在 blogProject 目录下（即 settings.py 所在的目录），原本就有一个 urls.py 文件，这是整个工程项目的 URL 配置文件。
# 而我们这里新建了一个 urls.py 文件，且位于 blog 应用下。这个文件将用于 blog 应用相关的 URL 配置，这样便于模块化管理。不要把两个文件搞混了
# 首页视图匹配的 URL 去掉域名后其实就是一个空的字符串。
# 对文章详情视图而言，每篇文章对应着不同的 URL。
# 比如我们可以把文章详情页面对应的视图设计成这个样子：
# 当用户访问 <网站域名>/posts/1/ 时，显示的是第一篇文章的内容，
# 而当用户访问 <网站域名>/posts/2/ 时，显示的是第二篇文章的内容，
# 这里数字代表了第几篇文章，也就是数据库中 Post 记录的 id

app_name = 'blog'
urlpatterns = [
    # path('', views.index, name='index'),
    # 前面已经说过每一个 URL 对应着一个视图函数，这样当用户访问这个 URL 时，
    # Django 就知道调用哪个视图函数去处理这个请求了。
    # 在 Django 中 URL 模式的配置方式就是通过 url 函数将 URL 和视图函数绑定。
    # 比如 path('', views.index, name='index')，它的第一个参数是 URL 模式，第二个参数是视图函数 index。
    # 对 url 函数来说，第二个参数传入的值必须是一个函数。
    # 而 IndexView 是一个类，不能直接替代 index 函数。
    # 好在将类视图转换成函数视图非常简单，只需调用类视图的 as_view() 方法即可（至于 as_view 方法究竟是如何将一个类转换成一个函数的目前不必关心，
    # 只需要在配置 URL 模式是调用 as_view 方法就可以了。
    # 具体的实现我们以后会专门开辟一个专栏分析类视图的源代码，到时候就能看出 django 使用的魔法了）。
    path('', views.IndexView.as_view(), name='index'),

    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    # 这里 'posts/<int:pk>/' 刚好匹配我们上面定义的 URL 规则。
    # 这条规则的含义是，以 posts/ 开头，后跟一个整数，并且以 / 符号结尾，如 posts/1/、 posts/255/ 等都是符合规则的，
    # 此外这里 <int:pk> 是 django 路由匹配规则的特殊写法，
    # 其作用是从用户访问的 URL 里把匹配到的数字捕获并作为关键字参数传给其对应的视图函数 detail。
    # 比如当用户访问 posts/255/ 时（注意 django 并不关心域名，而只关心去掉域名后的相对 URL），<int:pk> 匹配 255，
    # 那么这个 255 会在调用视图函数 detail 时被传递进去，其参数名就是冒号后面指定的名字 pk，
    # 实际上视图函数的调用就是这个样子：detail(request, pk=255)。
    # 我们这里必须从 URL 里捕获文章的 id，因为只有这样我们才能知道用户访问的究竟是哪篇文章
    # django 的路由匹配规则有很多类型，除了这里的 int 整数类型，还有 str 字符类型、uuid 等，
    # 可以通过官方文档了解：https://docs.djangoproject.com/en/2.2/topics/http/urls/#path-converters
    # 此外我们通过 app_name='blog' 告诉 django 这个 urls.py 模块是属于 blog 应用的，这种技术叫做视图函数命名空间
    # 我们看到 blog\urls.py 目前有两个视图函数，
    # 并且通过 name 属性给这些视图函数取了个别名，分别是 index、detail。
    # 但是一个复杂的 django 项目可能不止这些视图函数，例如一些第三方应用中也可能有叫 index、detail 的视图函数
    # 我们用品那个app_name来指定命名空间，如果你忘了在 blog\urls.py 中添加这一句，接下来你可能会得到一个 NoMatchReversed 异常

    path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    # 这个归档视图对应的 URL 和 detail 视图函数对应的 URL 是类似的，
    # 这在之前我们讲过，django 会从用户访问的 URL 中自动提取 URL 路径参数转换器 <type:name> 规则捕获的值，
    # 然后传递给其对应的视图函数。例如如果用户想查看 2017 年 3 月下的全部文章，
    # 他访问 /archives/2017/3/，那么 URL 转换器就会根据规则捕获到 2017 和 3 这两个整数，
    # 然后作为参数传给 archive 视图函数， archive 视图函数的实际调用为：archive(request, year=2017, month=3)
    # 接下来在 inclusions 文件夹下找到 archives 的模板，修改超链接的 href 属性，让用户点击超链接后跳转到文章归档页面
    # path('archives/<int:year>/<int:month>', views.archive, name='archive'),
    # path('categories/<int:pk>/', views.category, name='category'),
    path('categories/<int:pk>', views.CategoryView.as_view(), name='category'),
    path('tage/<int:pk>/', views.tag, name='tag'),
    path('search/', views.search, name='search'),
]

# 这个两行的函数体现了这个过程。它首先接受了一个名为 request 的参数，
# 这个 request 就是 django 为我们封装好的 HTTP 请求，它是类 HttpRequest 的一个实例。
# 然后我们便直接返回了一个 HTTP 响应给用户，这个 HTTP 响应也是 django 帮我们封装好的，
# 它是类 HttpResponse 的一个实例，只是我们给它传了一个自定义的字符串参数
# django 匹配 URL 模式是在 blogproject 目录（即 settings.py 文件所在的目录）的 urls.py 下的，
# 所以我们要把 blog 应用下的 urls.py 文件包含到 blogproject\urls.py 里去
