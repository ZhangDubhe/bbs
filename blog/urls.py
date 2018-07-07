#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/07/04 11:10
# @Author  : MJay_Lee
# @File    : urls.py
# @Contact : limengjiejj@hotmail.com


from django.conf.urls import url
from blog import views


urlpatterns = [
    url(r'(.*)/article/(\d+)/$',views.article_detail), # article_detail(request,username,article_nid)
    url(r'(.*)/(category|tag|archive)/(.*)/$',views.home), # home(request,username,*args)
    url(r'(.*)/$',views.home), # home(request,username)
]