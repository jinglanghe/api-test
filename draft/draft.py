#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/24 15:55
@DESC  : 
"""

import requests
import json
import urllib
url = "http://192.168.1.183/custom-user-dashboard-backend/group"

headers = {"content-type": "application/json",'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjMwMDAxLCJ1c2VyTmFtZSI6ImFkbWluIiwiZXhwIjoxNjI4OTEwNzY2LCJpYXQiOjE2Mjg3Mzc5NjZ9.o8AZMmXMZh95dlpHlR-FmvpqGhy3BgmpB6UFdQjqQa4'}

payload = {
    "name":"撒的发生",
    "note":"撒旦法撒旦法",
    "role":[1]
}

print(payload)
r = requests.request("post", url=url, headers=headers, json=payload)

print(r.url)
print(r.status_code)
print(r.request.method)
print(r.encoding)
# print(r.request.body)
if r.request.body:
    print(json.loads(r.request.body))
else:
    print(r.request.body)
# print(r.content)
# print(r.json())