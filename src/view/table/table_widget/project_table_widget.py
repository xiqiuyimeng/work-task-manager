# -*- coding: utf-8 -*-
from src.constant.table_constant import PROJECT_HEADER_LABELS
from src.view.table.table_widget.custom_table_widget import CustomTableWidget

_author_ = 'luwt'
_date_ = '2023/7/18 11:34'


class ProjectTableWidget(CustomTableWidget):

    def __init__(self, *args):
        super().__init__(PROJECT_HEADER_LABELS, *args)

    def do_fill_row(self, row_index, row_data, fill_create_time=True):
        self.setItem(row_index, 1, self.make_item(row_data.project_name, row_data.font_color,
                                                  row_data.background_color))
        if row_data.priority:
            self.setItem(row_index, 2, self.make_data_dict_item(row_data.priority))
        self.setItem(row_index, 3, self.make_item(row_data.font_color))
        self.setItem(row_index, 4, self.make_item(row_data.background_color))
