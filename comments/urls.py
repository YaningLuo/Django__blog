#!/usr/bin/python

# 编写者:沫
# 时间:09:06 下午
from django.urls import path

from . import views

app_name = 'comments'
urlpatterns = [
    path('comment/<int:post_pk>', views.comment, name='comment'),
]
