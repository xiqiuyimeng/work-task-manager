# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.enum.common_enum import get_dict_type_list
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init
from src.service.util.system_storage_util import Condition

_author_ = 'luwt'
_date_ = '2023/7/11 11:21'


table_name = 'data_dict'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    dict_name char(50) not null,
    font_color char(10) not null,
    background_color char(10) not null,
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


class DataDictSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, DataDict)

    def get_list_by_type(self, dict_type):
        condition = Condition(self.table_name).add('dict_type', dict_type)
        return self.select_by_order(condition=condition)

    def get_id_dict(self, dict_ids):
        condition = Condition(self.table_name).add('id', dict_ids, 'in')
        data_list = self.select(condition=condition)
        return {data.id: data for data in data_list}
