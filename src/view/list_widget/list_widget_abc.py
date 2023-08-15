# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QListWidget

from src.view.custom_widget.item_view_abc import ItemViewABC, DraggableItemViewABC

_author_ = 'luwt'
_date_ = '2023/7/10 14:53'


class ListWidgetABC(QListWidget, ItemViewABC):

    def __init__(self, *args):
        super().__init__(*args)
        # 设置列表项间距
        self.setSpacing(5)

    def fill_list_widget(self, *args):
        self.addItems(*args)


class DraggableListWidgetABC(ListWidgetABC, DraggableItemViewABC):

    def dropEvent(self, event) -> None:
        DraggableItemViewABC.dropEvent(self, event)
