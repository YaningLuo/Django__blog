from django.apps import AppConfig

# 这是我们使用startapp创建爱你blog应用是自动创建的代码，可以看到有一个 BlogConfig 类，其继承自 AppConfig 类
# 我们可以通过这是这个类中的一些属性来配置这个应用的一些特性的，比如name用来定义app的名字，需要和应用名包吃一直，不要改
# 要修改app在admin后台显示的名字，添加verbose_name属性，
# 同时我们此前在settings中注册应用时，是直接注册的app的名字blog，现在在 BlogConfig 类中对 app 做了一些配置，所以应该将这个类注册进去


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = '博客'
