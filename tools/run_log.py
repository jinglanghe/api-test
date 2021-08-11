#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/8/4 18:55
@DESC  : 
"""
import os
import datetime
import logging


class RunLog(object):
    def __init__(self):
        self.my_log()

    # 设置相应的日志格式
    def my_log(self):
        self.logger = logging.getLogger('mylog.log')
        if not self.logger.handlers:

            myStreamHandler = logging.StreamHandler()
            self.logger.setLevel(logging.DEBUG)
            format = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

            myStreamHandler.setFormatter(format)

            self.logger.addHandler(myStreamHandler)
        return self.logger


    def info(self, text):
        return self.logger.info(text)

    def debug(self, text):
        return self.logger.debug(text)

    def warning(self, text):
        return self.logger.warning(text)

    def error(self, text):
        return self.logger.error(text)

if __name__ == '__main__':
    ll = RunLog()
    ll.logger.info('info')
    ll.logger.debug('debug')
    ll.logger.warning('warning')
    ll.logger.error('error')