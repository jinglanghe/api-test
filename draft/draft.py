#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/24 15:55
@DESC  : 
"""

import os
import yaml
pwd = os.path.dirname(__file__)
with open(os.path.join(pwd, '../test_assert/test_base.yaml'), 'r', encoding='utf8') as h:
    api_base = yaml.safe_load(h)
    api_code_success = api_base['api']['response']['code']['success']
    api_msg_success = api_base['api']['response']['msg']['success']

    print(api_code_success, api_msg_success)

print('confict test')
print('2222222222222222')