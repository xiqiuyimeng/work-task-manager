# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit

_author_ = 'luwt'
_date_ = '2023/7/12 9:58'


class PageWidget(QWidget):
    """分页控件"""

    def __init__(self):
        # 总条数
        self.total_count_label: QLabel = ...
        # 每页条数
        self.page_size_combobox: QComboBox = ...
        self.page_size_label: QLabel = ...
        # 跳转页码
        self.jump_page_left_label: QLabel = ...
        self.jump_page_lineedit: QLineEdit = ...
        self.jump_page_right_label: QLabel = ...
        # 按钮组
        super().__init__()
