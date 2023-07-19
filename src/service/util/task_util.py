# -*- coding: utf-8 -*-
from src.enum.data_dict_enum import DataDictTypeEnum
from src.service.util.data_dict_cache_util import get_data_dict

_author_ = 'luwt'
_date_ = '2023/7/11 17:22'


def set_data_dict_obj(task):
    task.task_type = get_data_dict(DataDictTypeEnum.task_type.value[0], task.task_type_id)
    task.demand_person = get_data_dict(DataDictTypeEnum.demand_person.value[0], task.demand_person_id)
    task.priority = get_data_dict(DataDictTypeEnum.priority.value[0], task.priority_id)
    task.status = get_data_dict(DataDictTypeEnum.task_status.value[0], task.status_id)
    task.publish_status = get_data_dict(DataDictTypeEnum.publish_status.value[0], task.publish_status_id)
