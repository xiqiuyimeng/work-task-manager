# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QListWidgetItem

from src.view.list_widget.list_item_func import set_data_dict, get_data_dict
from src.view.list_widget.list_widget_abc import ListWidgetABC, DraggableListWidgetABC

_author_ = 'luwt'
_date_ = '2023/7/15 11:35'


class DataDictListWidget(ListWidgetABC):

    def __init__(self, open_detail_dialog, *args):
        self.open_detail_dialog = open_detail_dialog
        super().__init__(*args)

    def connect_signal(self):
        # 双击数据字典类型，进入详情页
        self.doubleClicked.connect(self.double_clicked_slot)

    def double_clicked_slot(self):
        item = self.currentItem()
        self.open_detail_dialog(item.text())


class DataDictSortListWidget(DraggableListWidgetABC):

    def __init__(self, *args):
        super().__init__(*args)

    def fill_list_widget(self, data_dict_list):
        for data_dict in data_dict_list:
            item = QListWidgetItem(data_dict.dict_name)
            set_data_dict(item, data_dict)
            self.addItem(item)

    def collect_data_dict_list(self):
        return [get_data_dict(self.item(row)) for row in range(self.count())]
