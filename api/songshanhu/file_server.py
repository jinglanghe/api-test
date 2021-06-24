#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/24 14:51
@DESC  : 
"""
from api.base import Base
import os


class FileServer(Base):
    # 文件服务器

    # 上传文件
    def upload_file(self, mod_id, file_name):
        path = self.api_path_list.get('api_path', {}).get('file_server', {}) \
            .get('upload', '/file_server/api/v1/files')
        payload = {
            'modId': mod_id
        }
        pwd = os.path.dirname(__file__)
        test_data_dir = os.path.join(pwd, '../../test_data')

        # 如果填的是一个绝对路径，那就直接用这个文件
        # 如果不是，就拿这个文件名去test_data下面找
        if os.path.exists(file_name):
            file_path = file_name
        else:
            file_path = os.path.join(test_data_dir, file_name)
        files = [
            (
                'file', (file_name, open(file_path, 'rb')))
        ]
        url = f'{self.base_url}{path}'
        return self.send_requests("post", url, data=payload, files=files)
