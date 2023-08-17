# -*- coding: utf-8 -*-
from PyQt6.QtGui import QBrush
from PyQt6.QtWidgets import QAbstractItemView

from src.view.dialog.color_dialog import get_color_from_rgba_str
from src.view.table.table_item.table_item import TableWidgetItem
from src.view.table.table_widget.tool_tip_table_widget import ToolTipTableWidget

_author_ = 'luwt'
_date_ = '2023/7/10 15:14'


class TableWidgetABC(ToolTipTableWidget):

    def setup_ui(self):
        super().setup_ui()
        # 交替行颜色
        self.setAlternatingRowColors(True)
        # 只允许单选
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def fill_table(self, *args):
        ...

    def make_item(self, text=None, text_color=None, background_color=None):
        item = TableWidgetItem(self)
        item.setText(text)
        if text_color:
            item.setForeground(QBrush(get_color_from_rgba_str(text_color)))
        if background_color:
            item.setBackground(QBrush(get_color_from_rgba_str(background_color)))
        return item

    def make_data_dict_item(self, data_dict):
        return self.make_item(data_dict.dict_name, data_dict.font_color, data_dict.background_color)

    def insert_row(self, row_index):
        self.insertRow(row_index)
        # 行高设为原行高的1.5倍，主要为了美观
        self.setRowHeight(row_index, round(self.rowHeight(row_index) * 1.5))
