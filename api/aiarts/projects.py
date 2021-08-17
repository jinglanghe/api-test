#!/usr/bin/python3
# -*- coding:UTF-8 -*-

"""
@Time    : 2021/6/23 20:56
@DESC  : 
"""
from api.base import Base
import os
from tools.read_yaml import ReadConfig
from tools.run_log import RunLog

logger = RunLog()


class Projects(Base):
    # 项目相关（项目-代码开发环境），后端接口封装
    def __init__(self):
        Base.__init__(self)
        pwd = os.path.dirname(__file__)
        self.read = ReadConfig()

    # 创建项目
    def create_project(self, payload: dict):
        path = self.api_path_list.get('api_path', {}).get('projects', {}) \
            .get('create_project', '/ai-arts/api/v1/projects')
        url = f'{self.base_url}{path}'
        logger.info(f'----------------------------创建项目----------------------------')
        return self.send_requests("post", url, json=payload)

    # 删除项目
    def delete_project(self, project_id):
        path = self.api_path_list.get('api_path', {}).get('projects', {}) \
            .get('delete_project', '/ai-arts/api/v1/projects/{id}')
        path = path.replace('{id}', str(project_id))
        url = f'{self.base_url}{path}'
        logger.info(f'----------------------------删除项目----------------------------')
        return self.send_requests("delete", url)

    # 获取项目详情
    def get_project(self, project_id):
        path = self.api_path_list.get('api_path', {}).get('projects', {}) \
            .get('get_project', '/ai-arts/api/v1/projects/{id}')
        path = path.replace('{id}', str(project_id))
        url = f'{self.base_url}{path}'
        logger.info(f'----------------------------获取项目详情----------------------------')
        return self.send_requests("get", url)

    # 获取项目列表
    def get_project_lists(self, page_num=1, page_size=99):
        path = self.api_path_list.get('api_path', {}).get('projects', {}) \
            .get('get_project_lists', '/ai-arts/api/v1/projects/list')
        url = f'{self.base_url}{path}'
        payload = {
            "pageNum": page_num,
            "pageSize": page_size,
            "sort": ""
        }
        logger.info(f'----------------------------获取项目列表----------------------------')
        return self.send_requests("get", url, params=payload)

    # 启动代码开发环境
    def start_code_lab(self, project_id, payload: dict):
        path = self.api_path_list.get('api_path', {}).get('projects', {}) \
            .get('start_code_lab', '/ai-arts/api/v1/projects/{id}/code-lab/start')
        path = path.replace('{id}', str(project_id))
        url = f'{self.base_url}{path}'
        logger.info(f'----------------------------启动代码开发环境----------------------------')
        return self.send_requests("post", url, json=payload)

    # 获取代码开发环境详情
    def get_code_lab(self, project_id, uid=0):
        path = self.api_path_list.get('api_path', {}).get('projects', {}) \
            .get('get_code_lab', '/ai-arts/api/v1/projects/{id}/code-lab')
        path = path.replace('{id}', str(project_id))
        url = f'{self.base_url}{path}?uid={uid}'
        logger.info(f'----------------------------获取代码开发环境详情----------------------------')
        return self.send_requests("get", url)

    # 获取代码开发环境列表
    def get_code_lab_list(self, project_id, group_id=None, page_num=1, page_size=99):
        path = self.api_path_list.get('api_path', {}).get('projects', {}) \
            .get('get_code_lab_list', '/ai-arts/api/v1/projects/{id}/code-lab/list')
        path = path.replace('{id}', str(project_id))
        url = f'{self.base_url}{path}'
        payload = {
            "pageNum": page_num,
            "pageSize": page_size,
            "groupId": group_id
        }
        logger.info(f'----------------------------获取代码开发环境列表----------------------------')
        if group_id is not None:
            return self.send_requests("get", url, params=payload)
        else:
            return self.send_requests("get", url)

    # 停止代码开发环境
    def stop_code_lab(self, project_id, run_id=None):
        path = self.api_path_list.get('api_path', {}).get('projects', {}) \
            .get('stop_code_lab', '/ai-arts/api/v1/projects/{id}/code-lab/stop')
        path = path.replace('{id}', str(project_id))
        url = f'{self.base_url}{path}'
        payload = {
            "runId": run_id
        }
        logger.info(f'----------------------------停止代码开发环境----------------------------')
        if run_id is not None:
            return self.send_requests("post", url, json=payload)
        else:
            return self.send_requests("post", url)

    # 获取数据集列表
    def get_dataset_list(self, payload: dict):
        path = self.api_path_list.get('api_path', {}).get('projects', {}) \
            .get('get_dataset_list', '/ai-arts/api/v1/datasets')
        url = f'{self.base_url}{path}'
        return self.send_requests("get", url, json=payload)
