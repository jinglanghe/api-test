#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/23 19:54
@DESC  : 
"""
from api.base import Base


class Scenes(Base):

    # 场景列表
    def get_scenes_list(self):
        path = self.api_path_list.get('scenes', {}).get('scenes', '/iqi/api/v1/scenes')
        url = f'{self.base_url}{path}'
        return self.send_requests("get", url)

    # 场景标签
    def get_scene_labels(self):
        path = self.api_path_list.get('scenes', {}).get('scene-labels', '/iqi/api/v1/scene-labels')
        url = f'{self.base_url}{path}'
        return self.send_requests("get", url)