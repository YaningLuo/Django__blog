#### `templates`用来存放模板,我们建立这样的文件夹结构的目的是把不同应用用到的模板隔离开来
#### 再一次强调 `templates` 目录位于项目根目录，而 `index.html` 位于 `templates\blog` 目录下，而不是 `blog`应用下，
#### 如果弄错了你可能会得到一个 `TemplateDoesNotExist` 异常。 如果遇到这个异常，请回来检查一下模板目录结构是否正确
#### 创建django后台管理员`python manage.py createsuperuser`