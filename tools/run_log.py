#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/8/4 18:55
@DESC  : 
"""
import os
import logging
from datetime import datetime

pwd = os.path.dirname(__file__)

now = datetime.now()  # current date and time
date_time = now.strftime("%Y-%m-%d_%H-%M-%S")


class RunLog(object):
    def __init__(self):
        self.logger = logging.getLogger('mylog')
        self.my_log()

    # 设置相应的日志格式
    def my_log(self):
        # 定义一个日志收集器
        if not self.logger.handlers:
            self.logger.setLevel('DEBUG')  # 设置收集器的级别，不设定的话，默认收集warning及以上级别的日志

            fmt = logging.Formatter('%(filename)s-%(lineno)d-%(asctime)s-%(levelname)s-%(message)s')  # 设置日志格式
            if not os.path.exists('../log'):
                os.makedirs('../log')
            log_file = os.path.join(pwd, f'../log/{date_time}.log')
            file_handler = logging.FileHandler(log_file, encoding='utf8')  # 设置日志处理器-输出到文件

            file_handler.setLevel("DEBUG")  # 设置日志处理器级别

            file_handler.setFormatter(fmt)  # 处理器按指定格式输出日志

            ch = logging.StreamHandler()  # 输出到控制台

            ch.setLevel("DEBUG")  # 设置日志处理器级别

            ch.setFormatter(fmt)  # 处理器按指定格式输出日志

            # 收集器和处理器对接，指定输出渠道
            self.logger.addHandler(file_handler)  # 日志输出到文件

            self.logger.addHandler(ch)  # 日志输出到控制台

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
    ll.logger.info('这是一个测试')
    ll.logger.debug('debug')
    ll.logger.warning('warning')
    ll.logger.error('error')
