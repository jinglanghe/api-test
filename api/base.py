#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/23 18:57
@DESC  : 
"""
import requests
import yaml
import os


class Base:
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), '../config/config.yaml'), 'r') as f:
            self.config = yaml.safe_load(f)

        with open(os.path.join(os.path.dirname(__file__), '../config/api_path_list.yaml'), 'r') as f:
            self.api_path_list = yaml.safe_load(f)

        http_style = self.config.get('http_style', {}).get('https', 'yes')
        if http_style == 'yes':
            http_style = 'https'
        else:
            http_style = 'http'

        ip = self.config.get('host', {}).get('ip')
        port = self.config.get('host', {}).get('port')
        login_api_path = self.api_path_list.get('login', '/iam/api/v1/users/login')
        self.base_url = f'{http_style}://{ip}:{port}'
        login_url = f'{http_style}://{ip}:{port}{login_api_path}'

        username = self.config.get('account', {}).get('username')
        password = self.config.get('account', {}).get('password')

        payload = {
            "userName": f"{username}",
            "password": f"{password}"
        }

        response = requests.post(login_url, json=payload, verify=False).json()

        self.token = response['data']['token']
        # 声明一个Session
        self.s = requests.Session()
        # 把token放入到session，每次参数都有token
        self.s.headers = {'authorization': f'Bearer {self.token}'}

    def send_requests(self, *args, **kwargs) -> dict:
        # 用session
        response = self.s.request(*args, **kwargs, verify=False)
        return response.json()


if __name__ == '__main__':
    test = Base()
    # data = {'userName': 'jinglang', 'password': '522810d987bdfa2e6459a3632eb835e8'}
    # r = requests.post(url='https://119.147.212.162:51080/iam/api/v1/users/login', json=data, verify=False)
    # print(r)
