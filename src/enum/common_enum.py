# -*- coding: utf-8 -*-
from enum import Enum

_author_ = 'luwt'
_date_ = '2023/7/10 17:40'


def get_dict_type_list():
    return [dict_type.value for dict_type in DictTypeEnum]


class DictTypeEnum(Enum):
    demand_person = '需求方'
    priority = '优先级'
    task_type = '任务类型'
    task_status = '任务状态'
    publish_status = '发版状态'
    publish_type = '发版信息类型'
