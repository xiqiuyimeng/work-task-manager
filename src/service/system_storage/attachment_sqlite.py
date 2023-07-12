# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init
from src.service.util.system_storage_util import Condition

_author_ = 'luwt'
_date_ = '2023/7/11 9:49'


table_name = 'attachment'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    attachment_name char(200) not null,
    attachment_content blob not null,
    task_id integer not null,
    item_order integer not null,
    create_time datetime not null,
    update_time datetime not null
    );''',
}


@init
@dataclass
class Attachment(BasicSqliteDTO):
    # 附件名称
    attachment_name: str = field(init=False, default=None)
    # 附件内容
    attachment_content: bytes = field(init=False, default=None)
    # 任务表id
    task_id: int = field(init=False, default=None)


class AttachmentSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, Attachment)

    def get_by_task_id(self, task_id):
        condition = Condition(self.table_name).add('task_id', task_id)
        return self.select_by_order(condition)
