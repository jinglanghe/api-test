#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/23 20:56
@DESC  : 
"""
from api.base import Base


class Apworkshop(Base):

    # 模型工厂（预置模型后端）
    # TODO
    def get_model_types(self):
        path = self.api_path_list.get('api_path', {}).get('apworkshop', {})\
            .get('model_types', '/iqi/api/v1/apworkshop/modelTypes')
        url = f'{self.base_url}{path}'
        return self.send_requests("get", url)
