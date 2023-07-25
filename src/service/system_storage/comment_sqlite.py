# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init
from src.service.util.system_storage_util import Condition

_author_ = 'luwt'
_date_ = '2023/7/11 10:17'


table_name = 'comment'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    comment text not null,
    task_id integer not null,
    item_order integer not null,
    create_time datetime not null,
    update_time datetime not null
    );''',
}


@init
@dataclass
class Comment(BasicSqliteDTO):
    # 备注信息
    comment: str = field(init=False, default=None)
    # 任务表id
    task_id: int = field(init=False, default=None)


class CommentSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, Comment)

    def get_by_task_id(self, task_id):
        condition = Condition(self.table_name).add('task_id', task_id)
        return self.select_by_order(condition=condition)
