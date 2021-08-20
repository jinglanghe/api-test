#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/24 15:55
@DESC  : 
"""

import requests


r = requests.request('get', "https://www.baidu.com")

print(r.elapsed.total_seconds()*1000)