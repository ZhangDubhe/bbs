#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/7 下午6:00
# @Author  : MJay_LEE
# @File    : comment_generator.py
# @Contact : limengjiejj@hotmail.com


class CommentGenerator:
    def __init__(self, floor_num, username, create_time, content, parent_comment):
        self.floor_num = floor_num
        self.username = username
        self.create_time = create_time
        self.content = content
        self.parent_comment = parent_comment

    def page_html(self):
        li_list = []

        # 评论头
        li_title = """
                <p>
                <span class="forloop_num">#{0}楼</span>
                <span>{1}</span>
                <a href="/blog/{2}">{2}</a>
                <span class="pull-right comment_reply">回复</span>
                </p>
                """.format(
            self.floor_num,
            self.create_time,
            self.username,
        )

        if self.parent_comment:
            li_list.append(li_title)
            li_list.append("""
                <p class="well">
                    <span>@{0}</span>
                    {1}
                </p>
                """.format(
                self.parent_comment.user.username,
                self.content
            ))
        else:
            li_list.append(li_title)
            li_list.append('<li class="list-group-item">{0}</li>'
                           .format(self.content))

        # 将生成的li标签，拼接成大的字符串
        comment_page_html = ''.join(li_list)
        return comment_page_html
