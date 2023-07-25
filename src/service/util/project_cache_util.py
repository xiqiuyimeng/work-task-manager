# -*- coding: utf-8 -*-
from src.enum.data_dict_enum import DataDictTypeEnum
from src.service.system_storage.project_sqlite import ProjectSqlite
from src.service.util.data_dict_cache_util import get_data_dict

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


# 当数据字典中优先级变化时，刷新缓存中优先级
def update_project_priority(new_id, origin_ids):
    for project in project_dict.values():
        if project.priority_id in origin_ids:
            project.priority_id = new_id
            project.priority = get_data_dict(DataDictTypeEnum.priority.value[0], new_id)
