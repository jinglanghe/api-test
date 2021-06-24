#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/24 15:55
@DESC  : 
"""
import yaml

with open('../test_data/test_scenes.yaml', 'r', encoding='utf8') as f:
  data = yaml.safe_load(f)
print(data)

