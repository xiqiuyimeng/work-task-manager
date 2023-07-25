# -*- coding: utf-8 -*-
from dataclasses import field, dataclass

from src.enum.data_dict_enum import DataDictTypeEnum
from src.service.system_storage.data_dict_sqlite import DataDict
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.data_dict_cache_util import get_data_dict
from src.service.util.dataclass_util import init
from src.service.util.system_storage_util import SelectCol, Condition

_author_ = 'luwt'
_date_ = '2023/7/10 17:32'


table_name = 'project'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    project_name char(50) not null,
    priority_id integer,
    project_desc text,
    font_color char(10),
    background_color char(10),
    item_order integer not null,
    create_time datetime not null,
    update_time datetime not null
    );''',
}


@init
@dataclass
class Project(BasicSqliteDTO):
    # 项目名称
    project_name: str = field(init=False, default=None)
    # 优先级 字典表id
    priority_id: int = field(init=False, default=None)
    # 优先级 字典表对象
    priority: DataDict = field(init=False, default=None)
    # 项目描述
    project_desc: str = field(init=False, default=None)
    # 字体颜色
    font_color: str = field(init=False, default=None)
    # 字体背景色
    background_color: str = field(init=False, default=None)


class ProjectSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, Project)

    def get_project_dict(self):
        project_list = self.select_by_order()
        project_dict = dict()
        for project in project_list:
            project_dict[project.id] = project
            if project.priority_id:
                project.priority = get_data_dict(DataDictTypeEnum.priority.value[0], project.priority_id)
        return project_dict

    def add_project(self, project):
        project.item_order = self.get_max_order()
        self.insert(project)

    def get_used_priority_ids(self, priority_ids):
        select_col = SelectCol(self.table_name).add('priority_id', distinct=True)
        condition = Condition(self.table_name).add('priority_id', priority_ids, 'in')
        return [project.priority_id for project in self.select(select_cols=select_col, condition=condition)]

    def update_priority_ids(self, new_id, origin_ids):
        update_project = Project()
        update_project.priority_id = new_id
        condition = Condition(self.table_name).add('priority_id', origin_ids, 'in')
        self.update_by_condition(update_project, condition)
