#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author:曾光
@file:utils.py
@time:2021/06/03
"""
import itsdangerous
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from .constants import ACCESS_TOKEN_EXPIRES


# 对openID进行加密以及解密
def generate_access_token(openid):
    """
    签名openid
    :param openid: 用户的openid
    :return: access_token
    """
    # serializer = Serializer(秘钥, 有效期秒)
    # serializer = Serializer(settings.SECRET_KEY, expires_in=ACCESS_TOKEN_EXPIRES)
    serializer = Serializer('121', expires_in=111)
    data = {"openid":openid}
    access_token = serializer.dumps(data)
    # 生成的access_token为bytes类型
    return access_token.decode()


def check_access_token(access_token):
    """
    解密access_token
    # 检验token
    # 验证失败，会抛出itsdangerous.BadData异常
    :param access_token: 加密后的access_token
    :return: 用户的openid
    """
    # serializer = Serializer(秘钥, 有效期秒)
    # serializer = Serializer(settings.SECRET_KEY, expires_in=ACCESS_TOKEN_EXPIRES)
    serializer = Serializer('121', expires_in=111)
    try:
        s = serializer.loads(access_token)
    except itsdangerous.BadData:
        openid = None
    else:
        openid = s.get('openid')
    return openid













