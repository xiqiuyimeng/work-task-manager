# -*- coding: utf-8 -*-
from src.constant.table_constant import MAIN_TABLE_HEADER_LABELS
from src.view.table.table_widget.custom_table_widget import CustomTableWidget

_author_ = 'luwt'
_date_ = '2023/7/10 15:34'


class WorkTaskManagerTableWidget(CustomTableWidget):

    def __init__(self, *args):
        super().__init__(MAIN_TABLE_HEADER_LABELS, *args)

    def do_fill_row(self, row_index, row_data, fill_create_time=True):
        self.setItem(row_index, 1, self.make_item(row_data.task_name))
        self.setItem(row_index, 2, self.make_project_item(row_data.project_info))
        self.setItem(row_index, 3, self.make_data_dict_item(row_data.task_type))
        self.setItem(row_index, 4, self.make_data_dict_item(row_data.demand_person))
        self.setItem(row_index, 5, self.make_data_dict_item(row_data.priority))
        self.setItem(row_index, 6, self.make_data_dict_item(row_data.status))
        self.setItem(row_index, 7, self.make_data_dict_item(row_data.publish_status))
        self.setItem(row_index, 8, self.make_item(row_data.start_time))
        self.setItem(row_index, 9, self.make_item(row_data.end_time))
        self.setItem(row_index, 10, self.make_item(row_data.time_duration))

    def make_project_item(self, project_info):
        return self.make_item(project_info.project_name, project_info.font_color,
                              project_info.background_color)
