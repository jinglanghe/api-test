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
import json

# urllib3.disable_warnings()
pwd = os.path.dirname(__file__)
logger = RunLog()


class Base:
    def __init__(self):
        self.token = ''

        # 读取配置
        with open(os.path.join(pwd, '../config/config.yaml'), 'r', encoding='utf8') as f:
            self.config = yaml.safe_load(f)

        with open(os.path.join(pwd, '../config/api_path_list.yaml'), 'r', encoding='utf8') as g:
            self.api_path_list = yaml.safe_load(g)

        # 读取配置


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
        with open(os.path.join(pwd, '../config/token.txt'), 'r', encoding='utf8') as i:
            self.token = str(i.read())

        # 如果token配置文件为空，则调用登录接口获取token，并写回token配置文件中
        # 如果token配置文件不为空，则直接使用token
        if self.token == '' or self.token is None:
            login_api_path = self.api_path_list.get('iam', {}).get('login', '/iam/api/v1/users/login')

            login_url = f'{self.base_url}{login_api_path}'

            username = self.config.get('account', {}).get('username')
            password = self.config.get('account', {}).get('password')

            payload = {
                "userName": f"{username}",
                "password": f"{password}"
            }
            urllib3.disable_warnings()
            response = requests.post(login_url, json=payload, verify=False).json()

            self.token = response['data']['token']
            with open(os.path.join(pwd, '../config/token.txt'), 'w', encoding='utf8') as j:
                j.write(self.token)
        return self.token

    # 封装request
    def send_requests(self, *args, **kwargs) -> dict:
        response = self.s.request(*args, **kwargs, verify=False)
        response.encoding = 'utf8'

        # logger.info(f'---------------------')
        logger.info(f'Full URL:  {response.request.url}, method:{response.request.method}')
        logger.info(f'Status code:  {response.status_code}')
        if response.request.body:
            logger.info(f'Request body:  {json.loads(response.request.body)}')
        else:
            logger.info(f'Request body:  {response.request.body}')
        logger.info(f'Response:  {response.json()}')
        logger.info(f'Elapsed time: {int(response.elapsed.total_seconds()*1000)} ms')
        return response.json()


if __name__ == '__main__':
    test = Base()
