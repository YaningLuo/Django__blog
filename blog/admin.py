from django.contrib import admin
from .models import Post, Category, Tag


# Register your models here.
# 要在后台注册我们自己创建的几个模型，这样 django admin 才能知道它们的存在
# 我们定义了一个PostAdmin来配置Post在admin后台展示一些形式
# list_display属性控制Post列表页展示的字段，此外还有一个fields属性来控制表单展现的字段
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    fields = ['title', 'body', 'excerpt', 'category', 'tags']

    # 接下来是填充创建时间，修改事假和文章作者值，之前提到的，文章作者应该自动设定为登录后台发布此文章的管理用户
    # 发布文章的过程实际上是一个http请求的过程，此前提到，django将http请求封装在HttpRequest对象中
    # 然后将其作为第一个参数传给视图函数(这里我们没有看到新增文章的视图，因为django admin已经自动帮我们生成了)
    # 当用户登录我们站点，django就会奖这个用户实例绑定到request.user属性上，我们可以通过request.user取到当前请求用户，如何将其关联发哦新创建的文章即可
    # PostAdmin继承自ModelAdmin，它有一个save——model方法，这个方法只有一行代码obj.save()
    # 它的作用是将此ModelAdmin关联注册到model实例(这里ModelAdmin关联注册的死Post)保存到数据库
    # 这个方法接受四个参数，其中前两个，一个是request，即此次的http请求对象，第二是obj，即此次创建的关联对象的实例
    # 通过复写此方法，就可以将request.user关联到创建的post实例行，如何将post数据保存倒数据库中
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)
    # 最后还剩下文章的创建时间和修改时间需要填充，一个想法我们可以沿用上面的思路，
    # 复写 save_model 方法，将创建的 post 对象关联当前时间，
    # 但是这存在一个问题，就是这样做的话只有通过 admin 后台创建的文章才能自动关联这些时间，
    # 但创建文章不一定是在 Admin，也可能通过命令行。这时候我们可以通过对 Post 模型的定制来达到目的
    # 首先，Model 中定义的每个 Field 都接收一个 default 关键字参数，
    # 这个参数的含义是，如果将 model 的实例保存到数据库时，对应的 Field 没有设置值，
    # 那么 django 会取这个 default 指定的默认值，将其保存到数据库。
    # 因此，对于文章创建时间这个字段，初始没有指定值时，默认应该指定为当前时间，所以刚好可以通过 default 关键字参数指定


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
