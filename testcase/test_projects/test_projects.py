#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/23 20:12
@DESC  : 
"""

from api.aiarts.projects import Projects
from jsonpath import *
from tools.read_yaml import ReadConfig
import os
import uuid
from datetime import datetime
from hamcrest import *
from tools.run_log import RunLog
import allure
import time

logger = RunLog()


@allure.feature('项目管理测试用例')
class TestProtects:

    def setup(self):
        self.projects = Projects()
        pwd = os.path.dirname(__file__)
        self.read = ReadConfig()
        self.test_data_projects = self.read.read_config(os.path.join(pwd, '../../test_data/test_projects.yaml'))
        self.now_time = datetime.strftime(datetime.now(), '%Y-%m-%d  %H:%M:%S')
        logger.info('执行项目管理测试用例')

        # 处理项目名称、描述、类型，得到payload
        # eg:
        # {'name':'Project_d9e1e2c5', 'description':'description d9e1e2c5,创建时间2021-08-13 15:50:41', 'type':'专家模式'}
        uuid_front_8 = str(uuid.uuid4())[:8]
        self.payload: dict = self.test_data_projects['data']['create_project']
        type_need = self.payload['type_pro']
        self.payload['name'] = f'Project_{uuid_front_8}'
        self.payload['description'] = f'description {uuid_front_8},  创建时间{self.now_time}'
        self.payload.pop('type_pro')
        self.payload.pop('type_preset')
        self.payload['type'] = type_need
        # 处理项目名称、描述、类型，得到payload

    @allure.story('项目列表接口，测试正常创建专家模式项目')
    def test_create_project(self):

        logger.info('测试创建专家模型项目')
        r = self.projects.create_project(self.payload)  # 创建项目

        r_list = self.projects.get_project_lists()  # 查询项目列表返回
        r_list_json: list = jsonpath(r_list, '$..data..items..name')  # 项目列表中所有的项目名称
        time.sleep(1)
        try:
            # assert_that(r_list_json, has_item(payload['name']))
            assert self.payload['name'] in r_list_json  # 判断创建的项目是否在列表中
        except Exception as e:
            logger.error(f"断言失败{e}, 添加失败，创建的项目没有在列表中。")
            # assert_that(r_list_json, has_item(payload['name']))
            assert self.payload['name'] in r_list_json
        else:
            logger.info("断言成功，项目添加成功。")

        #  数据清理
        project_id = jsonpath(r, '$.data.id')[0]
        self.projects.delete_project(project_id)
        logger.info(f"数据清理，删除项目，id {project_id}。")

    @allure.story('项目列表接口，测试项目列表默认按创建时间【倒序】排返回')
    def test_get_project_lists(self):
        logger.info('测试项目列表接口')
        r = self.projects.get_project_lists()  # 发送请求
        if jsonpath(r, '$..data..items..createdAt'):
            r_jsonpath: list = jsonpath(r, '$..data..items..createdAt')  # 获取所有项目的创建时间数组

            try:
                # assert_that(r_jsonpath, equal_to(sorted(r_jsonpath, reverse=True)))
                assert r_jsonpath == sorted(r_jsonpath, reverse=True)  # 原数组是否和倒序排序后的数组相等？
            except Exception as e:
                logger.error(f"断言失败{e}, 项目列表默认不是按倒序排返回。")
                assert r_jsonpath == sorted(r_jsonpath, reverse=True)
            else:
                logger.info("断言成功，项目列表默认按创建时间倒序排返回。")

    @allure.story('项目列表接口，正常删除项目')
    def test_delete_project(self):

        r_create = self.projects.create_project(self.payload)  # 创建项目
        project_id = jsonpath(r_create, '$.data.id')[0]
        time.sleep(1)

        self.projects.delete_project(project_id)  #  删除项目
        time.sleep(1)

        r_list = self.projects.get_project_lists()  # 查询项目列表返回
        r_list_json: list = jsonpath(r_list, '$..data..items..name')  # 项目列表中所有的项目名称
        try:
            assert self.payload['name'] not in r_list_json  # 判断创建的项目是否在列表中
        except Exception as e:
            logger.error(f"断言失败{e}, 删除项目失败，项目还是出现在列表中。")
            assert self.payload['name'] not in r_list_json
        else:
            logger.info("断言成功，删除项目成功。")

    # @allure.story('项目列表接口，获取项目详情')
    # def test_get_project(self):
    # TODO


