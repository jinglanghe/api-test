#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/24 12:08
@DESC  : 
"""
import yaml
class ReadConfig:
    def __init__(self):
        pass
    def rend_config(self, path):
        with open(path, 'r') as f:
            self.config = yaml.safe_load(f)
        return self.config