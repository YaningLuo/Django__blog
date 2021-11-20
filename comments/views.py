from blog.models import Post
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CommentForm


# Create your views here.


@require_POST
def comment(request, post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    # 这里我们使用了 django 提供的一个快捷函数 get_object_or_404，
    # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户
    post = get_object_or_404(Post, pk=post_pk)

    # django 将用户提交的数据封装在 request.POST 中，这是一个类字典对象。
    # 我们利用这些数据构造了 CommentForm 的实例，这样就生成了一个绑定了用户提交数据的表单
    form = CommentForm(request.POST)

    # 当调用 form.is_valid() 方法时，django 自动帮我们检查表单的数据是否符合格式要求。
    if form.is_valid():
        # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
        # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
        comment = form.save(commit=False)

        # 将评论和被评论的文章关联起来
        comment.post = post

        # 最终将评论数据保存进数据库，调用模型实例的 save 方法
        comment.save()

        messages.add_message(request, messages.SUCCESS, '发表成功', extra_tags='success')
        # 这里导入 django 的 messages 模块，使用 add_message 方法增加了一条消息，消息的第一个参数是当前请求，
        # 因为当前请求携带用户的 cookie，django 默认将详细存储在用户的 cookie 中。
        # 第二个参数是消息级别，评论发表成功的消息设置为 messages.SUCCESS，这是 django 已经默认定义好的一个整数，消息级别也可以自己定义。
        # 紧接着传入消息的内容，最后 extra_tags 给这条消息打上额外的标签，标签值可以在展示消息时使用，
        # 比如这里我们会把这个值用在模板中的 HTML 标签的 class 属性，增加样式

        # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
        # 然后重定向到 get_absolute_url 方法返回的 URL。
        return redirect(post)

    # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
    # 注意这里被评论的文章 post 也传给了模板，因为我们需要根据 post 来生成表单的提交地址
    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '发表失败,请修改之后发表', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)

# 这个评论视图相比之前的一些视图复杂了很多，主要是处理评论的过程更加复杂。具体过程在代码中已有详细注释，这里仅就视图中出现了一些新的知识点进行讲解。
# 首先视图函数被 require_POST 装饰器装饰，从装饰器的名字就可以看出，其作用是限制这个视图只能通过 POST 请求触发，因为创建评论需要用户通过表单提交的数据，而提交表单通常都是限定为 POST 请求，这样更加安全。
# 另外我们使用了 redirect 快捷函数。
# 这个函数位于 django.shortcuts 模块中，它的作用是对 HTTP 请求进行重定向（即用户访问的是某个 URL，但由于某些原因，服务器会将用户重定向到另外的 URL）。
# redirect 既可以接收一个 URL 作为参数，也可以接收一个模型的实例作为参数（例如这里的 post）。
# 如果接收一个模型的实例，那么这个实例必须实现了 get_absolute_url 方法，这样 redirect 会根据 get_absolute_url 方法返回的 URL 值进行重定向。
# 如果用户提交的数据合法，我们就将评论数据保存到数据库，否则说明用户提交的表单包含错误，我们将渲染一个 preview.html 页面，来展示表单中的错误，以便用户修改后重新提交
