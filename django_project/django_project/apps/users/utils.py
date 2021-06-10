#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author:曾光
@file:utils.py
@time:2021/05/10
"""
# 自定义用户后端
from django.contrib.auth.backends import ModelBackend
import re

from users.models import User


def get_user_by_account(account):
    try:
        # 校验输入的用户名
        if re.match(r'^1[3-9]\d{9}$', account):
            # username == 手机号
            user = User.objects.get(mobile=account)
        else:
            # username == 用户名
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileBackends(ModelBackend):
    # 重写authenticate方法
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 根据输入的账号查询用户
        user = get_user_by_account(username)
        if user and user.check_password(password):
            return user
        else:
            return None










