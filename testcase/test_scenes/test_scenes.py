#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/23 20:12
@DESC  : 
"""

from api.songshanhu.scenes import Scenes
from jsonpath import *
from tools.read_yaml import ReadConfig
import os


class TestScenes:

    def setup(self):
        self.scenes = Scenes()
        self.test_data = ReadConfig().rend_config(os.path.join(os.path.dirname(__file__), './test_data.yaml'))

    def test_get_scenes_list(self):
        r = self.scenes.get_scenes_list()
        assert r.get("code", "get failed") == 0

    def test_get_scene_labels(self):
        r = self.scenes.get_scene_labels()
        scene_labels = set(jsonpath(r, '$..data')[0])
        assert set(self.test_data.get('data').get('scene_labels')) == set(scene_labels)
