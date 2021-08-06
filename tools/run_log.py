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
        self.loger()

    # 设置相应的日志格式
    def loger(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # print('-----------------------')

        format = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
        # print(format)
        myStreamHandler = logging.StreamHandler()
        # print(myStreamHandler)
        myStreamHandler.setFormatter(format)
        # print(myStreamHandler)

        # print(myFileHandler)
        self.logger.addHandler(myStreamHandler)
        # print(self.logger)
        """
        <logging.Logger object at 0x0000000001F39AC8>
        10
        <logging.Formatter object at 0x00000000021E8E80>
        <logging.StreamHandler object at 0x00000000026D9940>
        <logging.StreamHandler object at 0x00000000026BA908>
        <logging.FileHandler object at 0x00000000026EA860>


        <logging.Logger object at 0x0000000002638E48>
        """

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