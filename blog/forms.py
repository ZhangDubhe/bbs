#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/07/02 10:04
# @Author  : MJay_Lee
# @File    : forms.py
# @Contact : limengjiejj@hotmail.com


from django import forms


# 登录
class LoginForm(forms.Form):

    # 用户名
    username = forms.CharField(
        label="用户名",
        min_length=3,
        max_length=12,
        error_messages={
            "required":"用户名不可为空",
            "min_length": "用户名最短3位",
            "max_length": "用户名最长12位"
        },
        widget=forms.widgets.TextInput(
            attrs={"class":"form-control"},
        )
    )

    # 密码
    password = forms.CharField(
        label="密码",
        min_length=4,
        max_length=12,
        error_messages={
            "required":"密码不能为空",
            "min_length": "密码最短3位",
            "max_length": "密码最长12位"
        },
        widget = forms.widgets.PasswordInput(
            attrs={"class": "form-control"}
        )
    )


from django.core.validators import RegexValidator,ValidationError
from . import models


def username_rule(value):
    if "fuck" in value:
        # 验证不通过，报错
        raise ValidationError("非法词汇")


# 注册
class RegisterForm(forms.Form):

    # 用户名
    username = forms.CharField(
        label="用户名",
        min_length=3,
        max_length=12,
        error_messages={
            "required":"用户名不能为空",
            "min_length": "用户名最短3位",
            "max_length": "用户名最长12位"
        },
        widget= forms.widgets.TextInput(
            attrs={"class":"form-control"}
        ),
        validators=[username_rule,] # 使用自定义校验规则函数
    )

    # 密码
    password = forms.CharField(
        label="密码",
        min_length=4,
        max_length=12,
        error_messages={
            "required":"密码不能为空",
            "min_length":"密码最短3位",
            "max_length":"密码最长12位"
        },
        widget = forms.widgets.PasswordInput(
            attrs={"class":"form-control"}
        )
    )

    # 确认密码
    re_password = forms.CharField(
        label="确认密码",
        min_length=4,
        max_length=12,
        error_messages={
            "required": "密码不能为空",
            "min_length": "密码最短3位",
            "max_length": "密码最长12位"
        },
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control"}
        )
    )

    # 手机号
    phone = forms.CharField(
        label="手机号",
        min_length=11,
        max_length=11,
        error_messages={
            "required":"手机号不能为空",
            "min_length":"手机号最少11位",
        },
        widget= forms.widgets.TextInput(
            attrs={"class":"form-control"}
        ),
        # 使用正则校验
        validators=[
            RegexValidator(r'^\d{11}$','手机号必须为11位数字'),
            RegexValidator(r'^1[356789][0-9]{9}$','手机格式不对')
        ]
    )

    # 局部钩子
    def clean_username(self):
        value = self.cleaned_data.get("username","")
        if "suck" in value:
            # 验证不通过，报错
            raise ValidationError("非法词汇")
        # 查重
        elif models.UserInfo.objects.filter(username=value):
            raise ValidationError("用户名已存在")
        else:
            # 验证通过，一定要返回值
            return value

    # 全局钩子
    def clean(self):
        password = self.cleaned_data.get("password","")
        re_password = self.cleaned_data.get("re_password","")
        if re_password and password == re_password:
            return self.cleaned_data
        else:
            err_msg = "两次密码不一致"
            self.add_error("re_password",err_msg)
            raise ValidationError(err_msg)