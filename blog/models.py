import markdown
from django.db import models
from django.contrib.auth.models import User  # 下面author导入的User模块
from django.utils import timezone  # 下面获取时间的模块
from django.urls import reverse
from django.utils.html import strip_tags


# pipenv run python manage.py makemigrations 和 pipenv run python manage.py migrate
# Create your models here.
# django把那一套数据库的语法转成了Python的语法形式，我们只要写Python代码就可以了
# django为我们提供了一套ORM(Object Relational Mapping)系统
# 这样django就可以把这个类翻译成数据库的操作语言，在数据库里常见一个名为Category的表格
# 代码翻译成数据库语言时其规则就是一个 Python 类对应一个数据库表格，类名即表名，类的属性对应着表格的列，属性名即列名


class Category(models.Model):  # 一个标准的Python类，继承了models.Model类，有一个name属性，是models.CharField的一个实例

    # django 要求模型必须继承 models.Model 类。
    # Category 只需要一个简单的分类名 name 就可以了。
    # CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    # CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    # 当然 django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
    # django 内置的全部类型可查看文档：
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    # 标签Tag也比较简单，和Category一样
    # 再次强调一定要继承models.Model
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    # 文章的数据库表稍微复杂一旦，主要涉及的字段更多
    # 我们给每个field都传入一个位置参数，参数值为field应该显示的名字(如果不传，django自动根据field名生成)
    # 这个参数的名字也叫 verbose_name，绝大部分field
    # 这个参数都位于第一个位置，但由于ForeignKey、ManyToManyField
    # 第一个参数必须传入其关联的Model，所以category、tags
    # 这些字段我们使用了关键字参数verbose_name
    # 文章标题
    title = models.CharField('标题', max_length=170)

    # 文章正文，我们使用TextField
    # 存储比较短的字符串可以使用CharField，但对于文章的正文来说可能会是一大段文本，所以使用TextField来存储打大段文本
    body = models.TextField('正文')

    # 这两个列表分别表示文章的创建时间和租后一次修改的时间，存储时间的字段用DateTimeField类型
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    # 这里default既可以指定一个常量值，也可以指定一个可调用(callable)对象
    # 我们指定timezone.now函数，这样如果没有指定created_time的值，django就会将其指定为timezone.now函数调用后的值
    # timezone.now是django提供的工具函数，返回当前时间，因为timezone模块中的函数会自动帮我们处理时区
    # 所以我们使用的是django为我们提供的timezone模块，而不是Python提供的dataTime模块来处理

    # 修改时间modified_time不能用default
    # 因为虽然第一次保存数据时，会根据默认值指定为当前时间，
    # 但是当模型数据第二次修改时，由于 modified_time 已经有值，即第一次的默认值，
    # 那么第二次保存时默认值就不会起作用了，如果我们不修改 modified_time 的值的话，其值永远是第一次保存数据库时的默认值
    # 每次保存模型时，都应该修改modified_time的值，每一个model都应该有一个save方法，这个方法包含将model数保存到数据库的逻辑
    # 通过覆写这个方法，在model被save到数据库前指定，modified_time的值为当前时间就可以
    modified_time = models.DateTimeField('修改时间')

    # 指定完modified_time的值后，别忘调用父类的save以执行保存回数据库的逻辑

    excerpt = models.CharField('摘要', max_length=200, blank=True)

    # 文章摘要，可以没有文章摘要，但默认情况下CharField要求我们必须存入数据，否则就会报错
    # 指定CharField的blank=Ture参数值后就可以允许空值了

    # 新增views字段
    views = models.PositiveIntegerField(default=0, editable=False)
    # views字段的类型为PositiveIntegerField,该类型的值只允许为正整数或0，初始化views的值为0，将editable参数设为false将不允许通过django admin后台编辑此字段内容

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        # 对于某些文章，自动摘取全n个字符作为摘要
        # 第一种方法是通过覆写模型的 save 方法，从正文字段摘取前 N 个字符保存到摘要字段
        # 第二种在README中
        # 在 创作后台开启，请开始你的表演 中我们提到过 save 方法中执行的是保存模型实例数据到数据库的逻辑，
        # 因此通过覆写 save 方法，在保存数据库前做一些事情，比如填充某个缺失字段的值
        # 其中 body 字段存储的是正文，excerpt 字段用于存储摘要。通过覆写模型的 save 方法，
        # 在数据被保存到数据库前，先从 body 字段摘取 N 个字符保存到 excerpt 字段中，从而实现自动摘要的目的

        # 首先实例化一个MarkDown类，用于渲染body的文本
        # 哟与摘要并不需要生成文本，所以去掉了目录的扩展
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ]
        )
        # 先将MarkDown文本渲染成html文本
        # strip_tags去掉html文本的全部html标签

        # 从文本摘要前54个字符赋给excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，
    # 所以我们使用的是 ForeignKey，即一对多的关联关系。
    # 且自 django 2.0 以后，ForeignKey 必须传入一个 on_delete 参数用来指定当关联的数据被删除时，
    # 被关联的数据的行为，我们这里假定当某个分类被删除时，该分类下全部文章也同时被删除，因此使用 models.CASCADE 参数，意为级联删除。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/2.2/topics/db/models/#relationships

    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='作者', blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    # 这里 User 是从 django.contrib.auth.models 导入的。django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程。

    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    # 首先是 Category 和 Tag 类，它们均继承自 models.Model 类，这是 django 规定的。
    # Category 和 Tag 类均有一个name 属性，用来存储它们的名称。
    # 由于分类名和标签名一般都是用字符串表示，因此我们使用了 CharField 来指定 name 的数据类型，
    # 同时 max_length 参数则指定 name 允许的最大长度，超过该长度的字符串将不允许存入数据库。
    # 除了 CharField ，django 还为我们提供了更多内置的数据类型，比如时间类型 DateTimeField、整数类型 IntegerField 等等
    #
    # 我们分别使用了两种关联数据库表的形式：ForeignKey和 ManyToManyField。
    # ForeignKey:表明一种一对多的关联关系。比如这里我们的文章和分类的关系，一篇文章只能对应一个分类，而一个分类下可以有多篇文章
    # ManyToManyField:表明一种多对多的关联关系，比如这里的文章和标签，一篇文章可以有多个标签，而一个标签下也可以有多篇文章

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        # 配置 model 的一些特性是通过 model 的内部类 Meta 中来定义
        # 这里通过 verbose_name 来指定对应的 model 在 admin 后台的显示名称，这里 verbose_name_plural 用来表示多篇文章时的复数显示形式。
        # 英语中，如果有多篇文章，就会显示为 Posts，表示复数，中文没有复数表现形式，所以定义为和 verbose_name一样
        ordering = ['-created_time']
        # ordering 属性用来指定文章排序方式，['-created_time'] 指定了依据哪个属性的值进行排序，这里指定为按照文章发布时间排序，且负号表示逆序排列。
        # 列表中可以有多个项，比如 ordering = ['-created_time', 'title'] 表示首先依据 created_time 排序，如果 created_time 相同，则再依据 title 排序

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 记得从django.urls导入reverse函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
        # 注意到 URL 配置中的 path('posts/<int:pk>/', views.detail, name='detail') ，
        # 我们设定的 name='detail' 在这里派上了用场。
        # 看到这个 reverse 函数，它的第一个参数的值是 'blog:detail'，意思是 blog 应用下的 name=detail 的函数，
        # 由于我们在上面通过 app_name = 'blog' 告诉了 django 这个 URL 模块是属于 blog 应用的，
        # 因此 django 能够顺利地找到 blog 应用下 name 为 detail 的视图函数，于是 reverse 函数会去解析这个视图函数对应的 URL，
        # 我们这里 detail 对应的规则就是 posts/<int:pk>/ int 部分会被后面传入的参数 pk 替换，
        # 所以，如果 Post 的 id（或者 pk，这里 pk 和 id 是等价的） 是 255 的话，
        # 那么 get_absolute_url 函数返回的就是 /posts/255/ ，这样 Post 自己就生成了自己的 URL
        # 实现我们detail视图函数

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
        # increase_views方法首选将自身对应的views字段的值+1(此时数据库的值还没改变)，让后调用save方法将更改后的值保存到数据库，注意update_fields参数来告诉django只更新数据库中views字段的值，以提高效率

