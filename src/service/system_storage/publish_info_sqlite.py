# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.enum.data_dict_enum import DataDictTypeEnum
from src.service.system_storage.data_dict_sqlite import DataDict
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.data_dict_cache_util import get_data_dict
from src.service.util.dataclass_util import init
from src.service.util.system_storage_util import Condition, SelectCol

_author_ = 'luwt'
_date_ = '2023/7/11 10:25'


table_name = 'publish_info'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    publish_type_id integer not null,
    publish_info text not null,
    task_id integer not null,
    item_order integer not null,
    create_time datetime not null,
    update_time datetime not null
    );''',
}


@init
@dataclass
class PublishInfo(BasicSqliteDTO):
    # 发版信息类型 字典表id
    publish_type_id: int = field(init=False, default=None)
    # 发版信息类型 字典表对象
    publish_type: DataDict = field(init=False, default=None)
    # 发版信息内容
    publish_info: str = field(init=False, default=None)
    # 任务表id
    task_id: int = field(init=False, default=None)


class PublishInfoSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, PublishInfo)

    def get_by_task_id(self, task_id):
        condition = Condition(self.table_name).add('task_id', task_id)
        publish_info_list = self.select_by_order(condition=condition)
        for publish_info in publish_info_list:
            publish_info.publish_type = get_data_dict(DataDictTypeEnum.publish_type.value[0],
                                                      publish_info.publish_type_id)
        return publish_info_list

    def add_publish_info_list(self, task_id, publish_info_list):
        for index, publish_info in enumerate(publish_info_list, start=1):
            publish_info.item_order = index
            publish_info.task_id = task_id
        self.batch_insert(publish_info_list)

    def del_publish_info_list(self, task_ids):
        condition = Condition(self.table_name).add('task_id', task_ids, 'in')
        self.delete_by_condition(condition)

    def update_publish_info_list(self, task_id, publish_info_list):
        self.del_publish_info_list((task_id,))
        if publish_info_list:
            self.add_publish_info_list(task_id, publish_info_list)

    def get_used_publish_type_ids(self, publish_type_ids):
        select_col = SelectCol(self.table_name).add('publish_type_id', distinct=True)
        condition = Condition(self.table_name).add('publish_type_id', publish_type_ids, 'in')
        return [publish_info.publish_type_id
                for publish_info in self.select(select_cols=select_col, condition=condition)]

    def update_publish_type_ids(self, new_id, origin_ids):
        update_publish_info = PublishInfo()
        update_publish_info.publish_type_id = new_id
        condition = Condition(self.table_name).add('publish_type_id', origin_ids, 'in')
        self.update_by_condition(update_publish_info, condition)
