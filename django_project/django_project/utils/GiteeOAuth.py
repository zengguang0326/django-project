#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author:曾光
@file:GiteeOAuth.py
@time:2021/05/26
"""
from urllib.parse import urlencode, parse_qs
import requests


class OAuthGitee(object):
    """
    Gitee认证辅助工具类
    """

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, state=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.state = state

    def get_gitee_url(self):
        # Gitee登录url参数组建
        data_dict = {
            'response_type': 'code',
            'scope':'user_info',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state
        }

        # 构建url
        gitee_url = 'https://gitee.com/oauth/authorize?' + urlencode(data_dict)

        return gitee_url

    # 获取access_token值
    def get_access_token(self, code):
        # 构建参数数据
        data_dict = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': code
        }

        # 构建url
        access_url = 'https://gitee.com/oauth/token?' + urlencode(data_dict)

        # 发送请求
        try:
            # response = requests.get(access_url)
            response = requests.post(access_url)

            # 提取数据
            # access_token=FE04************************CCE2&expires_in=7776000&refresh_token=88E4************************BE14
            data = response.json()

            # # 转化为字典
            # data = parse_qs(data)
        except:
            raise Exception('gitee请求失败')

        # 提取access_token
        access_token = data.get('access_token', None)

        if not access_token:
            raise Exception('access_token获取失败')

        return access_token

    # 获取open_id值

    def get_id(self, access_token):

        # 构建请求url
        url = 'https://gitee.com/api/v5/user?access_token={}'.format(access_token)

        # 发送请求
        try:
            response = requests.get(url)

            # 提取数据
            # callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} );
            # code=asdasd&msg=asjdhui  错误的时候返回的结果
            data = response.json()
        except:
            raise Exception('gitee请求失败')
        # 转化为字典
        try:
            # 获取openid
            openid = data.get('id')
        except:
            raise Exception('id获取失败')

        return openid











