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
        self.api_base = self.read.read_config(os.path.join(pwd, '../../test_assert/test_base.yaml'))
        self.api_code_success = self.api_base['api']['response']['code']['success']
        self.api_msg_success = self.api_base['api']['response']['msg']['success']
        # test_projects的测试数据 test_data_projects
        self.test_data_projects: dict = self.read.read_config(os.path.join(pwd, '../../test_data/test_projects.yaml'))
        self.now_time = datetime.strftime(datetime.now(), '%Y-%m-%d  %H:%M:%S')
        logger.info('执行项目管理测试用例')

        # 处理项目名称、描述、类型，得到payload
        # eg:
        # {'name':'Project_d9e1e2c5', 'description':'description d9e1e2c5,创建时间2021-08-13 15:50:41', 'type':'专家模式'}
        uuid_front_8 = str(uuid.uuid4())[:8]
        self.create_project_payload: dict = self.test_data_projects['data']['create_project']
        type_need = self.create_project_payload['type_pro']
        self.create_project_payload['name'] = f'Project_{uuid_front_8}'
        self.create_project_payload['description'] = f'description {uuid_front_8},  创建时间{self.now_time}'
        self.create_project_payload.pop('type_pro')
        self.create_project_payload.pop('type_preset')
        self.create_project_payload['type'] = type_need
        # 处理项目名称、描述、类型，得到payload

        # 启动代码开发环境的参数
        self.start_code_lab_payload: dict = self.test_data_projects['data']['start_code_lab']

        # 代码开发环境状态码列表
        self.code_lab_status: dict = self.test_data_projects['data']['code_lab_status']

        # 以下测试用例都将先创建一个项目再进行测试
        # self.r_create_project = self.projects.create_project(self.create_project_payload)
        # self.project_id = jsonpath(self.r_create_project, '$.data.id')[0]

    # def teardown(self):
    #     #  数据清理
    #     self.projects.delete_project(self.project_id)
    #     logger.info(f"数据清理，删除项目，id {self.project_id}")

    @allure.story('项目列表接口，测试正常创建专家模式项目')
    def test_create_project(self):

        logger.info('测试创建专家模型项目')
        r = self.projects.create_project(self.create_project_payload)  # 创建项目

        r_list = self.projects.get_project_lists()  # 查询项目列表返回
        r_list_json: list = jsonpath(r_list, '$..data..items..name')  # 项目列表中所有的项目名称

        try:
            # assert_that(r_list_json, has_item(payload['name']))
            assert self.create_project_payload['name'] in r_list_json  # 判断创建的项目是否在列表中
        except Exception as e:
            logger.error(f"断言失败{e}, 添加失败，创建的项目没有在列表中")
            # assert_that(r_list_json, has_item(payload['name']))
            assert self.create_project_payload['name'] in r_list_json
        else:
            logger.info("断言成功，项目添加成功")

        # 数据清理
        project_id = jsonpath(r, '$.data.id')[0]
        self.projects.delete_project(project_id)
        logger.info(f"数据清理，删除项目，id {project_id}")

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
                logger.error(f"断言失败{e}, 项目列表默认不是按倒序排返回")
                assert r_jsonpath == sorted(r_jsonpath, reverse=True)
            else:
                logger.info("断言成功，项目列表默认按创建时间倒序排返回")

    @allure.story('项目列表接口，正常删除项目')
    def test_delete_project(self):
        logger.info('测试删除项目接口')
        r_create_project = self.projects.create_project(self.create_project_payload)  # 创建项目
        project_id = jsonpath(r_create_project, '$.data.id')[0]

        self.projects.delete_project(project_id)  # 删除项目

        r_list = self.projects.get_project_lists()  # 查询项目列表返回
        r_total = jsonpath(r_list, '$.data.total')[0]
        if r_total != 0:
            r_list_json: list = jsonpath(r_list, '$..data..items..name')  # 项目列表中所有的项目名称
            try:
                assert self.create_project_payload['name'] not in r_list_json  # 判断创建的项目是否在列表中
            except Exception as e:
                logger.error(f"断言失败{e}, 删除项目失败，项目还是出现在列表中")
                assert self.create_project_payload['name'] not in r_list_json
            else:
                logger.info("断言成功，删除项目成功")
        else:
            try:
                assert r_total == 0  # 判断创建的项目是否在列表中
            except Exception as e:
                logger.error(f"断言失败{e}, 删除项目失败，项目还是出现在列表中")
                assert r_total == 0
            else:
                logger.info("断言成功，删除项目成功")

    @allure.story('项目列表接口，获取项目详情')
    def test_get_project(self):
        logger.info('测试获取项目详情接口')
        r_create_project = self.projects.create_project(self.create_project_payload)  # 创建项目
        project_id = jsonpath(r_create_project, '$.data.id')[0]

        r = self.projects.get_project(project_id)
        status = jsonpath(r, '$..data..status')[0]

        try:
            assert status == 'ready'  # 项目状态应为ready
        except Exception as e:
            logger.error(f"断言失败{e}, 项目状态不是ready")
            assert status == 'ready'
        else:
            logger.info("断言成功，项目状态是ready")

        #  数据清理
        self.projects.delete_project(project_id)
        logger.info(f"数据清理，删除项目，id {project_id}")

    @allure.story('项目列表接口，启动代码开发环境')
    def test_code_lab(self):

        logger.info('测试创建代码开发环境')

        r_create_project = self.projects.create_project(self.create_project_payload)  # 创建项目
        project_id = jsonpath(r_create_project, '$.data.id')[0]

        r = self.projects.start_code_lab(project_id, self.start_code_lab_payload)
        code = jsonpath(r, '$.code')[0]
        message = jsonpath(r, '$.message')[0]

        try:
            assert code == self.api_code_success and message == self.api_msg_success  # 接口返回应为 code:0, msg:success
        except Exception as e:
            logger.error(f"断言失败{e}, 启动代码开发环境失败")
            assert code == self.api_code_success and message == self.api_msg_success
        else:
            logger.info("断言成功，启动代码开发环境成功")

        lab_status = 0
        time_flag = 0
        # 查询job的状态，当任务状态变为运行中或超过60s未运行中，则测试用例判断为失败
        while lab_status != self.code_lab_status['running'] and time_flag < 60:
            time_flag += 1
            r_status = self.projects.get_code_lab(project_id)
            lab_status = jsonpath(r_status, '$.data.status')[0]
            # 当代码开发环境状态变为失败时，轮询退出，测试用例也判断为失败
            if lab_status == self.code_lab_status['error']:
                lab_status = self.code_lab_status['error']
                break
            time.sleep(1)

        try:
            assert lab_status == self.code_lab_status['running']  # 项目状态应为ready
        except Exception as e:
            logger.error(f"断言失败{e}, 代码开发环境状态不为running")
            assert lab_status == self.code_lab_status['running']
        else:
            logger.info("断言成功，代码开发环境状态为running")
        finally:
            # 停止代码开发环境
            run_id = jsonpath(r_status, '$.data.runId')[0]
            r_stop = self.projects.stop_code_lab(project_id, run_id)
            code_stop = jsonpath(r_stop, '$.code')[0]
            message_stop = jsonpath(r_stop, '$.message')[0]

            try:
                assert code_stop == self.api_code_success and message_stop == self.api_msg_success
                # 接口返回应为 code:0, msg:success
            except Exception as e:
                logger.error(f"断言失败{e}, 停止代码开发环境失败")
                assert code_stop == self.api_code_success and message_stop == self.api_msg_success
            else:
                logger.info("断言成功，停止代码开发环境成功")

            #  数据清理
            self.projects.delete_project(project_id)
            logger.info(f"数据清理，删除项目，id {project_id}")

    @allure.story('项目列表接口，获取同组所有用户环境')
    def test_get_code_lab_list(self):
        logger.info('测试获取同组所有用户环境接口')
        r_create_project = self.projects.create_project(self.create_project_payload)  # 创建项目
        project_id = jsonpath(r_create_project, '$.data.id')[0]
        group_id = jsonpath(r_create_project, '$.data.groupId')[0]
        r = self.projects.get_code_lab_list(project_id, group_id)
        r_data: dict = jsonpath(r, '$.data')[0]

        # TODO 断言的条件可以再想想
        try:
            assert 'items' in r_data.keys()  # 接口有返回items字段
        except Exception as e:
            logger.error(f"断言失败{e}, 获取同组所有用户环境成功")
            assert 'items' in r_data.keys()
        else:
            logger.info("断言成功，获取同组所有用户环境失败")
