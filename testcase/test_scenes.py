#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/23 20:12
@DESC  : 
"""
import pytest

from api.songshanhu.scenes_management import ScenesManagement


class TestScenesManagement:

    def setup(self):
        self.scenes_management = ScenesManagement()

    def test_get_scenes_list(self):
        r = self.scenes_management.get_scenes_list()
        assert r.get("code", "get failed") == 0


