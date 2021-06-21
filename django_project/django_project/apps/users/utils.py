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
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from . import constants
from itsdangerous import BadData

from users.models import User


def check_verify_email_token(token):
    serializer = Serializer(settings.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    try:
        data = serializer.loads(token)
    except BadData:
        return None
    else:
        user_id = data.get('user_id')
        email = data.get('email')
        try:
            user = User.objects.get(id=user_id, email=email)
        except User.DoseNotExist:
            return None
        else:
            return user


def generate_verify_email_url(user):
    """
    生成邮箱激活链接
    :param user: 当前登录用户
    :return: http://www.meiduo.site:8000/emails/verification/?token=eyJhbGciOiJIUzUxMiIsImlhdCI6MTU1ODA2MDE0MSwiZXhwIjoxNTU4MTQ2NTQxfQ.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6InpoYW5namllc2hhcnBAMTYzLmNvbSJ9.y1jaafj2Mce-LDJuNjkTkVbichoq5QkfquIAhmS_Vkj6m-FLOwBxmLTKkGG0Up4eGGfkhKuI11Lti0n3G9XI3Q
    """
    # s = Serializer(settings.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)

    serializer = Serializer(settings.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    # serializer = Serializer('121', expires_in=111)
    data = {"user_id": user.id, "email": user.email}
    token = serializer.dumps(data)
    # 生成的access_token为bytes类型
    url = settings.EMAIL_VERIFY_URL + '?token=' + token.decode()
    return url


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










