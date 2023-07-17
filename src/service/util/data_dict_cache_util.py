# -*- coding: utf-8 -*-
from src.service.system_storage.data_dict_sqlite import DataDictSqlite

_author_ = 'luwt'
_date_ = '2023/7/17 9:39'


all_data_dict = dict()


def init_data_dict():
    global all_data_dict
    all_data_dict = DataDictSqlite().get_all_data_dict()


def get_data_dict(dict_type):
    return all_data_dict.get(dict_type)


def update_data_dict(dict_type, data_list):
    all_data_dict[dict_type] = data_list
