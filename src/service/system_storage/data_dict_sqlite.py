# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List

from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init
from src.service.util.group_util import group_model_dict
from src.service.util.system_storage_util import Condition, transactional

_author_ = 'luwt'
_date_ = '2023/7/11 11:21'


table_name = 'data_dict'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    dict_name char(50) not null,
    font_color char(10),
    background_color char(10),
    dict_type char(20) not null,
    item_order integer not null,
    create_time datetime not null,
    update_time datetime not null
    );''',
}


@init
@dataclass
class DataDict(BasicSqliteDTO):
    # 字典名称
    dict_name: str = field(init=False, default=None)
    # 字典类型，枚举值中的value
    dict_type: str = field(init=False, default=None)
    # 字体颜色
    font_color: str = field(init=False, default=None)
    # 字体背景色
    background_color: str = field(init=False, default=None)
    # 非数据库字段，在保存数据时使用
    bind_data_list: List = field(init=False, default=None)


class DataDictSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, DataDict)

    def get_all_data_dict(self):
        data_dict_list = self.select_by_order()
        # 按类型分组
        return group_model_dict(data_dict_list, lambda x: x.dict_type, lambda x: x.id)

    @transactional
    def save_data_dict(self, data_dict_list):
        # id集合，插入数据集合，更新数据集合
        id_list, insert_list, update_list = list(), list(), list()
        # 首先处理顺序问题
        for order, data_dict in enumerate(data_dict_list, start=1):
            data_dict.item_order = order
            if data_dict.id:
                id_list.append(data_dict.id)
                update_list.append(data_dict)
            else:
                insert_list.append(data_dict)
        # 删除不在 id list 中的数据
        condition = Condition(self.table_name).add('dict_type', data_dict_list[0].dict_type)
        condition.add('id', id_list, 'not in')
        self.delete_by_condition(condition=condition)
        # 插入新的数据
        if insert_list:
            self.batch_insert(insert_list)
        # 更新数据
        if update_list:
            self.batch_update(update_list)
