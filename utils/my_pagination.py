#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/06/25 19:30
# @Author  : MJay_Lee
# @File    : my_pagination.py
# @Contact : limengjiejj@hotmail.com


class Pagination:
    """
    使用说明:
    data = models.Publisher.objects.all()
    total_num = data.count()
    current_page = request.GET.get("page")
    from utils import my_pagination
    page_obj = my_pagination.Pagination(total_num, current_page, 'publisher_list', per_page_data_num=20)
    page_html = page_obj.page_tool_html()

    为了显示效果，show_page_num最好使用奇数
    """
    def __init__(self,total_num,current_page,url_prefix,per_page_data_num=10,show_page_num=11):
        """

        :param total_num: 数据的总条数
        :param per_page_data_num: 每一页显示多少条数据
        :param current_page:  当前访问的页码
        :param url_prefix: a标签的URL前缀,如’book_list‘或'publisher_list'
        :param show_page_num: 页面上最多显示多少个页码
        """

        self.total_num = total_num
        self.url_prefix = url_prefix

        self.per_page_data_num = per_page_data_num
        self.show_page_num = show_page_num

        # 通过初始化传入的值计算得到的值
        self.half_show_page_num = self.show_page_num // 2
        # 当前数据总共需要多少页码
        total_page,more = divmod(self.total_num,self.per_page_data_num)
        # 如果有余数，就把页码数+1
        if more:
            total_page += 1
        self.total_page = total_page
        # 对传进来的值进行有效性校验
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        # 若当前页码数小于1，默认展示首页
        if current_page < 1:
            current_page = 1
        # 若当前页码数大于总页码数,默认展示最后一页的数据
        if current_page > self.total_page:
            current_page = total_page
        self.current_page = current_page

        # 根据当前取值，计算分页器需要展示的页码范围
        if self.current_page - self.half_show_page_num <= 1:
            start_page = 1
            end_page = show_page_num
        elif self.current_page + self.half_show_page_num >= total_page:
            start_page = self.current_page - self.half_show_page_num + 1
            end_page = total_page
        else:
            start_page = self.current_page - self.half_show_page_num
            end_page = self.current_page + self.half_show_page_num
        self.start_page = start_page
        self.end_page = end_page # 分页器最大页数

        # 分页器最大页数大于数据总共需要的页数，那么执行如下：
        if self.end_page > total_page:
            # 分页器最大页数修正为数据总共所需要的页数
            self.end_page = total_page


    @property
    def data_start(self):
        # 返回当前页应该从哪开始切数据
        return (self.current_page -1) * self.per_page_data_num


    @property
    def data_end(self):
        # 返回当前页应该切到哪里为止
        return self.current_page * self.per_page_data_num


    def page_tool_html(self):
        li_list = []
        # 添加bootstrap样式头
        li_list.append("""
        <nav aria-label="Page navigation">
            <ul class="pagination">
        """)
        # 添加首页
        li_list.append('<li><a href="/{}/?page=1">首页</a></li>'.format(self.url_prefix))
        # 添加上一页
        if self.current_page <= 1:  # 若当前页没有“上一页"的值时
            prev_li = '<li class="disabled"><a><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            prev_li = '<li><a href="/{0}/?page={1}"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.url_prefix,self.current_page - 1)
        li_list.append(prev_li)
        # 分页器的正体
        for i in range(self.start_page, self.end_page + 1):  # range取值，顾头不顾尾，取尾页值需+1
            # 当前页码高亮显示
            if i == self.current_page:
                tmp = '<li class="active"><a href="/{0}/?page={1}">{1}</a></li>'.format(self.url_prefix,i)
            else:
                tmp = '<li><a href="/{0}/?page={1}">{1}</a></li>'.format(self.url_prefix,i)
            li_list.append(tmp)
        # 添加下一页
        if self.current_page >= self.total_page:  # 若当前页没有“下一页"的值时
            next_li = '<li class="disabled"><a><span aria-hidden="true">&raquo;</span></a></li>'
        else:
            next_li = '<li><a href="/{0}/?page={1}"><span aria-hidden="true">&raquo;</span></a></li>'.format(self.url_prefix,self.current_page + 1)
        li_list.append(next_li)
        # 添加尾页
        li_list.append('<li><a href="/{0}/?page={1}">尾页</a></li>'.format(self.url_prefix,self.total_page))
        # 添加bootstrap样式尾
        li_list.append("""
                    </ul>
                </nav>
                """)

        # 将生成的li标签，拼接成大的字符串
        pagination_html = ''.join(li_list)
        return pagination_html