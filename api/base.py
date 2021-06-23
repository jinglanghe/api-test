#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/23 18:57
@DESC  : 
"""
import requests
import yaml


class Base:
    def __init__(self):
        with open('../config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
            # print(config)

        http_style = config.get('http_style', {}).get('https', 'yes')
        if http_style == 'yes':
            http_style = 'https'
        else:
            http_style = 'http'

        ip = config.get('host', {}).get('ip', '119.147.212.162')
        port = config.get('host', {}).get('port', '51080')
        url = f'{http_style}://{ip}:{port}/iam/api/v1/users/login'
        # print(url)

        username = config.get('account', {}).get('username', 'jinglanghe')
        password = config.get('account', {}).get('password', '522810d987bdfa2e6459a3632eb835e8')

        payload = {
            "userName": f"{username}",
            "password": f"{password}"
        }
        # print(payload)

        response = requests.post(url, json=payload, verify=False).json()
        self.token = response['data']['token']
        # 声明一个Session
        self.s = requests.Session()
        # 把token放入到session，每次参数都有token
        self.s.params = {'access_token': self.token}
        print(self.s.params)

    def send_requests(self, *args, **kwargs):
        # 用session
        response = self.s.request(*args, **kwargs)
        return response.json()


if __name__ == '__main__':
    test = Base()
    # data = {'userName': 'jinglang', 'password': '522810d987bdfa2e6459a3632eb835e8'}
    # r = requests.post(url='https://119.147.212.162:51080/iam/api/v1/users/login', json=data, verify=False)
    # print(r)
