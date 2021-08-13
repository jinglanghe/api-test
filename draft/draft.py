#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/24 15:55
@DESC  : 
"""

from hamcrest import *

list_a = [ 'f8e35b43', '0cef7c62', '是Ss12-_AS', '第十个手动if无偶诶你偶读未发文', '第九个时代峻峰危机期间欧文', '第八个发窘文件覅偶全文翻', '第七个清热贵而且荣女', '第七个水电费加豆腐囧文件', '第六个的空间哥今儿个接耳机', '第五个的附近噢我微积分琼文附近噢我', '第四个圣诞节卢浮宫科荣', '第三个电饭锅和如果', '第二个项目looklook', '创建一个项目试试看']

pro = 'Project_e4877286'
assert_that(pro, is_in(list_a))