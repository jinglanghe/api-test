#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/23 20:12
@DESC  : 
"""

from api.songshanhu.scenes import Scenes
from api.songshanhu.file_server import FileServer
from jsonpath import *
from tools.read_yaml import ReadConfig
import os
import uuid
from random import choice


class TestScenes:

    def setup(self):
        self.scenes = Scenes()
        self.file_server = FileServer()
        pwd = os.path.dirname(__file__)
        self.read = ReadConfig()
        self.test_data_scenes = self.read.read_config(os.path.join(pwd, '../../test_data/test_scenes.yaml'))
        self.test_file_server = self.read.read_config(os.path.join(pwd, '../../test_data/test_file_server.yaml'))

    def test_get_scenes_list(self):
        r = self.scenes.get_scenes_list()
        assert r.get("code", "get failed") == 0

    def test_get_scene_labels(self):
        r = self.scenes.get_scene_labels()
        scene_labels = set(jsonpath(r, '$..data')[0])  # 系统中一般预置了["det_cls", "ocr", "seg"]的标签
        assert set(self.test_data_scenes.get('data').get('scene_labels')) == set(scene_labels)


    def test_create_scene(self):
        payload: dict = self.test_data_scenes.get('data').get('create_scenes')

        scene_name = payload.get('name')
        scene_flag = payload.get('sceneFlag')
        image_name = payload.get('imageName')

        # 填null则为'scene' + uuid随机名称
        if scene_name is None:
            scene_name = 'scene' + str(uuid.uuid4())[:8]
            payload['name'] = scene_name

        # 填null则从scene_labels随机选择
        if scene_flag is None:
            scene_labels = self.test_data_scenes.get('data').get('scene_labels')
            scene_flag = choice(scene_labels)
            payload['sceneFlag'] = scene_flag

        # 如果输入的路径是绝对路径，截取文件名
        # 如果不是绝对路径，则用自己的文件名。从test_data里面找改文件
        if os.path.exists(image_name):
            payload['imageName'] = os.path.basename(image_name)

        r = self.scenes.create_scene(payload)
        assert r.get('code', "create failed") == 0
