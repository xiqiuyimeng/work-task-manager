# -*- coding: utf-8 -*-
from enum import Enum

from src.constant.data_dict_dialog_constant import PRIORITY, TASK_TYPE, DEMAND_PERSON, TASK_STATUS, PUBLISH_STATUS, \
    PUBLISH_TYPE, PRIORITY_VALUES, TASK_TYPE_VALUES, DEMAND_PERSON_VALUES, TASK_STATUS_VALUES, PUBLISH_STATUS_VALUES, \
    PUBLISH_TYPE_VALUES

_author_ = 'luwt'
_date_ = '2023/7/15 11:07'


class DataDictTypeEnum(Enum):
    priority = 'priority', PRIORITY, PRIORITY_VALUES
    task_type = 'task_type', TASK_TYPE, TASK_TYPE_VALUES
    demand_person = 'demand_person', DEMAND_PERSON, DEMAND_PERSON_VALUES
    task_status = 'task_status', TASK_STATUS, TASK_STATUS_VALUES
    publish_status = 'publish_status', PUBLISH_STATUS, PUBLISH_STATUS_VALUES
    publish_type = 'publish_type', PUBLISH_TYPE, PUBLISH_TYPE_VALUES


def get_data_dict_type_names():
    return [data_dict_type.value[1] for data_dict_type in DataDictTypeEnum]


def get_data_dict_type_by_name(type_name):
    for data_dict_type in DataDictTypeEnum:
        if data_dict_type.value[1] == type_name:
            return data_dict_type.value
    return DataDictTypeEnum.priority.value



