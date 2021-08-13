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
logger = RunLog()


class TestScenes:

    def setup(self):
        self.projects = Projects()
        pwd = os.path.dirname(__file__)
        self.read = ReadConfig()
        self.test_data_projects = self.read.read_config(os.path.join(pwd, '../../test_data/test_projects.yaml'))
    '''
    def test_get_scenes_list(self):
        r = self.scenes.get_scenes_list()
        assert r.get("code", "get failed") == 0

    def test_get_scene_labels(self):
        r = self.scenes.get_scene_labels()
        scene_labels = set(jsonpath(r, '$..data')[0])  # 系统中一般预置了["det_cls", "ocr", "seg"]的标签
        assert set(self.test_data_scenes.get('data').get('scene_labels')) == set(scene_labels)
    '''
    # def test_create_pro_project(self):
    #     payload: dict = self.test_data_projects.get('data').get('create_project')
    #
    #     # 当前时间，用于写在描述当中
    #     now_time = str(datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
    #     payload['name'] = f'Project_{str(uuid.uuid4())[:8]}'
    #     payload['description'] = f'创建项目， {now_time}'
    #     payload['type'] = 0
    #     print(payload)
    #     r = self.projects.create_project(payload)
    #     # TODO

    def test_get_project_lists(self):
        r = self.projects.get_project_lists()
        r_jsonpath : list = jsonpath(r, '$..data..items..createdAt') # 获取所有项目的创建时间数组

        try:
            assert_that(r_jsonpath, equal_to(sorted(r_jsonpath, reverse=True))) # 原数组是否和倒序排序后的数组相等？
        except Exception as e:
            logger.error(f"断言失败{e}, 项目列表默认不是按倒序排返回。")
            assert_that(r_jsonpath, equal_to(sorted(r_jsonpath, reverse=True)))
        else:
            logger.info("断言成功，项目列表默认按创建时间倒序排返回。")

