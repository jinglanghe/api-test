#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/23 18:57
@DESC  : 
"""
import requests
import yaml
import os
import urllib3
from tools.run_log import RunLog

urllib3.disable_warnings()
pwd = os.path.dirname(__file__)


class Base:
    def __init__(self):
        self.token = ''

        # 读取配置
        with open(os.path.join(pwd, '../config/config.yaml'), 'r') as f:
            self.config = yaml.safe_load(f)

        # 读取配置
        with open(os.path.join(pwd, '../config/api_path_list.yaml'), 'r') as g:
            self.api_path_list = yaml.safe_load(g)

        # 确认是http还是https
        http_style = self.config.get('http_style', {}).get('https', 'yes')
        if http_style == 'yes':
            http_style = 'https'
        else:
            http_style = 'http'

        # 读取配置，ip和端口，拼出url
        ip = self.config.get('host', {}).get('ip')
        port = self.config.get('host', {}).get('port')
        self.base_url = f'{http_style}://{ip}:{port}'

        # 调用登录方法，获取token
        self.login_get_token()

        # 声明session，后续使用
        self.s = requests.Session()
        # 把token放入到session，每次参数都有token
        self.s.headers = {'authorization': f'Bearer {self.token}'}

    # 登录方法，获取token
    def login_get_token(self):
        # 读token配置文件
        with open(os.path.join(pwd, '../config/token.txt'), 'r') as h:
            self.token = str(h.read())

        # 如果token配置文件为空，则调用登录接口获取token，并写回token配置文件中
        # 如果token配置文件不为空，则直接使用token
        if self.token == '' or self.token is None:
            login_api_path = self.api_path_list.get('login', '/iam/api/v1/users/login')

            login_url = f'{self.base_url}{login_api_path}'

            username = self.config.get('account', {}).get('username')
            password = self.config.get('account', {}).get('password')

            payload = {
                "userName": f"{username}",
                "password": f"{password}"
            }

            response = requests.post(login_url, json=payload, verify=False).json()

            self.token = response['data']['token']
            with open(os.path.join(pwd, '../config/token.txt'), 'w') as h:
                h.write(self.token)
        return self.token

    # 封装request
    def send_requests(self, *args, **kwargs) -> dict:
        # 用session
        urllib3.disable_warnings()

        response = self.s.request(*args, **kwargs, verify=False)

        run_log = RunLog()
        run_log.info(f'---------------------')
        run_log.info(f'Full URL:  {response.request.url}, method:{args[0]}')
        run_log.info(f'Status code:  {response.status_code}')
        # run_log.info(f'Request parameters:  {response.request.body}')
        run_log.info(response.json())
        return response.json()


if __name__ == '__main__':
    test = Base()
    # with open(os.path.join(pwd, '../config/token.txt'), 'r') as i:
    #     token = str(i.read())
    # print(token == '')
    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjMwMDAxLCJ1c2VyTmFtZSI6ImFkbWluIiwiZXhwIjoxNj' \
    #         'I4NzM0Mjc3LCJpYXQiOjE2Mjg1NjE0Nzd9.AydUw7WuO9nx3SozevT6Z8yiOoXE0XJ78PJkx2khfqU'
    # with open(os.path.join(pwd, '../config/token.txt'), 'w') as j:
    #     j.write(token)
    # data = {'userName': 'jinglang', 'password': '522810d987bdfa2e6459a3632eb835e8'}
    # r = requests.post(url='https://119.147.212.162:51080/iam/api/v1/users/login', json=data, verify=False)
    # print(r)
