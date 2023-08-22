# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List

from src.service.system_storage.attachment_sqlite import Attachment
from src.service.system_storage.data_dict_sqlite import DataDict
from src.service.system_storage.project_sqlite import Project
from src.service.system_storage.publish_info_sqlite import PublishInfo
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init
from src.service.util.project_cache_util import get_project
from src.service.util.system_storage_util import Condition, SelectCol
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
    start_time datetime,
    end_time datetime,
    time_duration char(20),
    publish_status_id integer not null,
    content text,
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
    # 发版信息列表
    publish_info_list: List[PublishInfo] = field(init=False, default=None)


class TaskSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, Task)

    def get_task_names(self):
        select_col = SelectCol(self.table_name).add('task_name')
        return [task.task_name for task in self.select(select_cols=select_col)]

    def search_task(self, search_param: BasicTask, page):
        condition = Condition(self.table_name)
        # 拼接条件
        if search_param.task_name:
            condition.add('task_name', search_param.task_name, 'like')
        if search_param.project_id:
            condition.add('project_id', search_param.project_id)
        if search_param.priority_id:
            condition.add('priority_id', search_param.priority_id)
        if search_param.task_type_id:
            condition.add('task_type_id', search_param.task_type_id)
        if search_param.demand_person_id:
            condition.add('demand_person_id', search_param.demand_person_id)
        if search_param.status_id:
            condition.add('status_id', search_param.status_id)
        if search_param.publish_status_id:
            condition.add('publish_status_id', search_param.publish_status_id)
        if search_param.start_time:
            condition.add('start_time', search_param.start_time, 'ge')
        if search_param.end_time:
            condition.add('end_time', search_param.end_time, 'le')

        self.select(return_type=BasicTask, condition=condition, order_by='start_time', sort_order='desc', page=page)
        task_list = page.data
        if task_list:
            for task in task_list:
                # 项目
                task.project_info = get_project(task.project_id)
                # 数据字典
                set_data_dict_obj(task)

    def get_task_detail(self, task_id):
        condition = Condition(self.table_name).add('id', task_id)
        task_detail = self.select_one(condition=condition)
        # 项目
        task_detail.project_info = get_project(task_detail.project_id)
        # 字典项
        set_data_dict_obj(task_detail)
        return task_detail

    def add_task(self, task):
        task.item_order = self.get_max_order()
        self.insert(task)

    def get_task_name(self, task_id):
        select_col = SelectCol(self.table_name).add('task_name')
        condition = Condition(self.table_name).add('id', task_id)
        task = self.select_one(select_cols=select_col, condition=condition)
        return task.task_name if task else None

    def get_used_foreign_ids(self, foreign_ids, col_name, get_foreign_id_func):
        select_col = SelectCol(self.table_name).add(col_name, distinct=True)
        condition = Condition(self.table_name).add(col_name, foreign_ids, 'in')
        return [get_foreign_id_func(task) for task in self.select(select_cols=select_col, condition=condition)]

    def get_used_project_ids(self, project_ids):
        return self.get_used_foreign_ids(project_ids, 'project_id', lambda task: task.project_id)

    def get_used_priority_ids(self, priority_ids):
        return self.get_used_foreign_ids(priority_ids, 'priority_id', lambda task: task.priority_id)

    def get_used_task_type_ids(self, task_type_ids):
        return self.get_used_foreign_ids(task_type_ids, 'task_type_id', lambda task: task.task_type_id)

    def get_used_demand_person_ids(self, demand_person_ids):
        return self.get_used_foreign_ids(demand_person_ids, 'demand_person_id', lambda task: task.demand_person_id)

    def get_used_task_status_ids(self, status_ids):
        return self.get_used_foreign_ids(status_ids, 'status_id', lambda task: task.status_id)

    def get_used_publish_status_ids(self, publish_status_ids):
        return self.get_used_foreign_ids(publish_status_ids, 'publish_status_id', lambda task: task.publish_status_id)

    def update_data_dict_ids(self, new_id, origin_ids, property_name):
        update_task = Task()
        setattr(update_task, property_name, new_id)
        condition = Condition(self.table_name).add(property_name, origin_ids, 'in')
        self.update_by_condition(update_task, condition)

    def update_priority_ids(self, new_id, origin_ids):
        self.update_data_dict_ids(new_id, origin_ids, 'priority_id')

    def update_task_type_ids(self, new_id, origin_ids):
        self.update_data_dict_ids(new_id, origin_ids, 'task_type_id')

    def update_demand_person_ids(self, new_id, origin_ids):
        self.update_data_dict_ids(new_id, origin_ids, 'demand_person_id')

    def update_task_status_ids(self, new_id, origin_ids):
        self.update_data_dict_ids(new_id, origin_ids, 'status_id')

    def update_publish_status_ids(self, new_id, origin_ids):
        self.update_data_dict_ids(new_id, origin_ids, 'publish_status_id')
