# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/7/17 9:27'


def add_group_dict(group_dict, get_group_key, child_group_key, data):
    key = get_group_key(data)
    data_group_dict = group_dict.get(key)
    # 如果之前没存储过，那么创建dict
    if data_group_dict is None:
        data_group_dict = dict()
        group_dict[key] = data_group_dict
    data_group_dict[child_group_key(data)] = data


def group_model_dict(data_list, get_group_key, child_group_key):
    model_dict = dict()
    for data in data_list:
        add_group_dict(model_dict, get_group_key, child_group_key, data)
    return model_dict
