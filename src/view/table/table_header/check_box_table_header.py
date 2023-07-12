# -*- coding: utf-8 -*-
from src.view.table.table_header.table_header_abc import TableHeaderABC
from src.view.table.table_header.table_header_style_delegate import TableHeaderStyleDelegate

_author_ = 'luwt'
_date_ = '2023/7/10 15:22'


class CheckBoxHeader(TableHeaderABC):
    """普通复选框表头"""

    def __init__(self, header_labels, parent_table):
        self.header_labels = header_labels
        # 表头1行
        super().__init__(1, len(header_labels) + 1, parent_table, parent_table)
        # 设置代理
        self.setItemDelegate(TableHeaderStyleDelegate())

    def setup_header_items(self):
        for col, header_text in enumerate(self.header_labels, start=1):
            self.setItem(0, col, self.make_item(header_text))
