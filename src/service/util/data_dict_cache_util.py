# -*- coding: utf-8 -*-
from src.service.system_storage.data_dict_sqlite import DataDictSqlite

_author_ = 'luwt'
_date_ = '2023/7/17 9:39'


# 数据字典，两层结构，第一层为字典类型，第二层字典 id：字典对象
all_data_dict = dict()


def init_data_dict():
    global all_data_dict
    all_data_dict = DataDictSqlite().get_all_data_dict()


def get_data_dict_list(dict_type):
    data_dict = all_data_dict.get(dict_type)
    return data_dict.values() if data_dict else tuple()


def update_data_dict(dict_type, data_dict):
    all_data_dict[dict_type] = data_dict


def get_data_dict(dict_type, dict_id):
    data_dict = all_data_dict.get(dict_type)
    return data_dict.get(dict_id) if data_dict else None
