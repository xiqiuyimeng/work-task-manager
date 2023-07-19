# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List

from src.service.system_storage.attachment_sqlite import Attachment
from src.service.system_storage.comment_sqlite import Comment
from src.service.system_storage.data_dict_sqlite import DataDict
from src.service.system_storage.project_sqlite import Project
from src.service.system_storage.publish_info_sqlite import PublishInfo
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init
from src.service.util.project_cache_util import get_project
from src.service.util.system_storage_util import Condition
from src.service.util.task_util import set_data_dict_obj

_author_ = 'luwt'
_date_ = '2023/7/10 17:31'


table_name = 'task'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    project_id integer not null,
    task_name char(50) not null,
    task_type_id integer not null, 
    demand_person_id integer not null,
    priority_id integer not null,
    status_id integer not null,
    start_time datetime not null,
    end_time datetime not null,
    time_duration char(20) not null,
    publish_status_id integer not null,
    content text not null,
    item_order integer not null,
    create_time datetime not null,
    update_time datetime not null
    );''',
}


@init
@dataclass
class BasicTask(BasicSqliteDTO):
    # 项目表id
    project_id: int = field(init=False, default=None)
    # 项目对象
    project_info: Project = field(init=False, default=None)
    # 任务名称
    task_name: str = field(init=False, default=None)
    # 任务类型 字典表id
    task_type_id: int = field(init=False, default=None)
    # 任务类型 字典对象
    task_type: DataDict = field(init=False, default=None)
    # 需求方 字典表id
    demand_person_id: int = field(init=False, default=None)
    # 需求方 字典对象
    demand_person: DataDict = field(init=False, default=None)
    # 优先级 字典表id
    priority_id: int = field(init=False, default=None)
    # 优先级 字典对象
    priority: DataDict = field(init=False, default=None)
    # 状态 字典表id
    status_id: int = field(init=False, default=None)
    # 状态 字典对象
    status: DataDict = field(init=False, default=None)
    # 开始时间
    start_time: str = field(init=False, default=None)
    # 结束时间
    end_time: str = field(init=False, default=None)
    # 耗时
    time_duration: str = field(init=False, default=None)
    # 发版状态 字典表id
    publish_status_id: int = field(init=False, default=None)
    # 发版状态 字典表对象
    publish_status: DataDict = field(init=False, default=None)


@init
@dataclass
class Task(BasicTask):
    # 详细说明
    content: str = field(init=False, default=None)
    # 附件列表
    attachment_list: List[Attachment] = field(init=False, default=None)
    # 评论列表
    comment_list: List[Comment] = field(init=False, default=None)
    # 发版信息列表
    publish_info_list: List[PublishInfo] = field(init=False, default=None)


class TaskSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, Task)

    def get_task_list(self):
        task_list = self.select_by_order(return_type=BasicTask)
        if task_list:
            for task in task_list:
                # 项目
                task.project_info = get_project(task.project_id)
                # 数据字典
                set_data_dict_obj(task)
        return task_list

    def get_task_detail(self, task_id):
        condition = Condition(self.table_name).add('id', task_id)
        task_detail = self.select_one(condition=condition)
        # 项目
        task_detail.project_info = get_project(task_detail.project_id)
        # 字典项
        set_data_dict_obj(task_detail)
        return task_detail

    def count_task_by_project_ids(self, project_ids):
        condition = Condition(self.table_name).add('project_id', project_ids, 'in')
        return self.select_count(condition)
