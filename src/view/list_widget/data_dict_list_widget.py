# -*- coding: utf-8 -*-
from src.view.list_widget.list_widget_abc import ListWidgetABC

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
