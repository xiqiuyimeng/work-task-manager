# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.service.system_storage.data_dict_sqlite import DataDict, DataDictSqlite
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init
from src.service.util.system_storage_util import Condition

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
        publish_info_list = self.select_by_order(condition)
        publish_type_ids = {publish_info.publish_type_id for publish_info in publish_info_list}
        publish_type_id_dict = DataDictSqlite().get_id_dict(publish_type_ids)
        for publish_info in publish_info_list:
            publish_info.publish_type = publish_type_id_dict.get(publish_info.publish_type_id)
        return publish_info_list
