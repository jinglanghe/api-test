#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/23 19:54
@DESC  : 
"""
from api.base import Base
from api.songshanhu.file_server import FileServer
from tools.read_yaml import ReadConfig
import os
import uuid
from random import choice


class Scenes(Base):
    # 场景管理
    def __init__(self):
        Base.__init__(self)
        pwd = os.path.dirname(__file__)
        self.read = ReadConfig()
        self.file_server = FileServer()
        self.test_data_scenes = self.read.read_config(os.path.join(pwd, '../../test_data/test_scenes.yaml'))
        self.test_data_file_server = self.read.read_config(os.path.join(pwd, '../../test_data/test_file_server.yaml'))

    # 场景列表
    def get_scenes_list(self):
        path = self.api_path_list.get('scenes', {}).get('scenes', '/iqi/api/v1/scenes')
        url = f'{self.base_url}{path}'
        return self.send_requests("get", url)

    # 场景标签
    def get_scene_labels(self):
        path = self.api_path_list.get('scenes', {}).get('scene_labels', '/iqi/api/v1/scene-labels')
        url = f'{self.base_url}{path}'
        return self.send_requests("get", url)

    # 创建场景
    def create_scene(self, payload: dict):
        path = self.api_path_list.get('scenes', {}).get('scene', '/iqi/api/v1/scenes')
        data_dict = self.test_data_file_server.get('data').get('upload')
        mod_id = data_dict.get('mod_id')

        # 上传场景图片，获取返回的下载链接downloadLink
        upload_r = self.file_server.upload_file(mod_id, payload.get('imageName'))
        payload['imagePath'] = upload_r.get('data').get('downloadLink')

        url = f'{self.base_url}{path}'
        return [self.send_requests("post", url, json=payload), payload['imagePath'], url]