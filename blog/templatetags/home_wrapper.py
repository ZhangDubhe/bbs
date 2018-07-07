#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/07/05 14:26
# @Author  : MJay_Lee
# @File    : home_wrapper.py
# @Contact : limengjiejj@hotmail.com


from django import template
from blog import models

register = template.Library()


@register.inclusion_tag("left_panel.html")
def wrapper(username):
    user_obj = models.UserInfo.objects.filter(
        username=username).first()  # QuerySet()对象转化为对象
    # 找到合法用户
    # 找到该用户的博客属性:提取博客标题，博客主题
    blog = user_obj.blog

    # 左侧面板数据

    # 分类筛选
    # 类型分类
    from django.db.models import Count
    category_list = models.Category.objects.filter(blog=blog).annotate(
        num=Count("article")).values("title", "num")

    # 标签分类
    tag_list = models.Tag.objects.filter(blog=blog).annotate(
        num=Count("article")).values("title", "num")

    # 日期分类
    archive_list = models.Article.objects.filter(user=user_obj).extra(
        select={
            "year_month": "DATE_FORMAT(create_time,'%%Y-%%m')"}).values(
        "year_month").annotate(num=Count("nid")).values("year_month", "num")

    return {
        "username": username,
        "category_list": category_list,
        "tag_list": tag_list,
        "archive_list": archive_list
    }
