#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/23 20:12
@DESC  : 
"""
import pytest
from api.songshanhu.scenes import Scenes
from jsonpath import *

class TestScenes:

    def setup(self):
        self.scenes = Scenes()

    def test_get_scenes_list(self):
        r = self.scenes.get_scenes_list()
        assert r.get("code", "get failed") == 0

    def test_get_scene_labels(self):
        r = self.scenes.get_scene_labels()
        scene_labels = jsonpath(r, '$..data')[0]
        print(scene_labels)



