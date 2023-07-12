# -*- coding: utf-8 -*-
from src.service.system_storage.data_dict_sqlite import DataDictSqlite
from src.service.util.db_id_generator_util import init_id_generator
from src.service.util.system_storage_util import get_sqlite_sequence, release_connection

_author_ = 'luwt'
_date_ = '2023/7/10 12:48'


def init_data():
    try:
        # 触发数据字典建表操作
        DataDictSqlite()
        # 初始化id生成器
        init_id_generator(get_sqlite_sequence)
    finally:
        # 主线程使用的连接需要手动释放
        release_connection()
