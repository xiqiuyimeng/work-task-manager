# -*- coding: utf-8 -*-
from src.service.system_storage.project_sqlite import ProjectSqlite

_author_ = 'luwt'
_date_ = '2023/7/18 13:57'

# 项目数据
project_dict = dict()


def init_project_dict():
    global project_dict
    project_dict = ProjectSqlite().get_project_dict()


def get_project_dict_list():
    return project_dict.values()


def update_project_dict(project):
    project_dict[project.id] = project


def remove_project(project_ids):
    for project_id in project_ids:
        del project_dict[project_id]


def get_project(project_id):
    return project_dict.get(project_id)
