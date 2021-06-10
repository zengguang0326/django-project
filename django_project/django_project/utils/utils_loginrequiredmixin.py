#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author:曾光
@file:utils_loginrequiedmixin.py
@time:2021/06/09
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http

from django_project.utils.response_code import RETCODE


class LoginRequiredJsonMixin(LoginRequiredMixin):
    """用户未登录响应json信息"""
    def handle_no_permission(self):
        return http.JsonResponse({'code':RETCODE.SESSIONERR, 'errmsg':'用户未登录'})










