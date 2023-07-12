# -*- coding: utf-8 -*-
from dataclasses import field, dataclass

from src.service.system_storage.data_dict_sqlite import DataDict, DataDictSqlite
from src.service.system_storage.sqlite_abc import BasicSqliteDTO, SqliteBasic
from src.service.util.dataclass_util import init
from src.service.util.system_storage_util import SelectCol, Condition

_author_ = 'luwt'
_date_ = '2023/7/10 17:32'


table_name = 'project'

sql_dict = {
    'create': f'''create table if not exists {table_name}
    (id integer primary key autoincrement,
    project_name char(50) not null,
    priority_id integer not null,
    font_color char(10) not null,
    background_color char(10) not null,
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
    # 字体颜色
    font_color: str = field(init=False, default=None)
    # 字体背景色
    background_color: str = field(init=False, default=None)


class ProjectSqlite(SqliteBasic):

    def __init__(self):
        super().__init__(table_name, sql_dict, Project)

    def get_project_id_dict(self, project_ids):
        select_col = SelectCol(self.table_name).add('id').add('project_name')\
            .add('font_color').add('background_color')
        condition = Condition(self.table_name).add('id', project_ids, 'in')
        project_list = self.select(select_cols=select_col, condition=condition)
        return {project.id: project for project in project_list}

    def get_project_list(self):
        project_list = self.select_by_order()
        priority_ids = {project.priority_id for project in project_list}
        priority_id_dict = DataDictSqlite().get_id_dict(priority_ids)
        for project in project_list:
            project.priority = priority_id_dict.get(project.priority_id)
        return project_list
