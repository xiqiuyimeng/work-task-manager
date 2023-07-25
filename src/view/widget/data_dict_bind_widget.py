# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QFrame, QLabel, QGridLayout, QComboBox

from src.constant.data_dict_dialog_constant import DATA_DICT_BIND_ARROW_TEXT, DATA_DICT_COMBOBOX_PLACEHOLDER_TEXT
from src.view.custom_widget.scrollable_widget import ScrollArea

_author_ = 'luwt'
_date_ = '2023/7/25 9:40'


class DataDictBindWidget(ScrollArea):

    def __init__(self, origin_data_dict_list, data_dict_list):
        super().__init__()
        self.origin_data_dict_list = origin_data_dict_list
        self.data_dict_list = data_dict_list
        self.canvas_content_frame: QFrame = ...
        self.canvas_content_layout: QGridLayout = ...
        self.setup_ui()

    def setup_ui(self):
        # 画布，用来承载控件
        self.canvas_content_frame = QFrame()
        self.canvas_content_frame.setObjectName('data_dict_bind_canvas_content_frame')
        # 设置画布控件
        self.set_canvas_widget(self.canvas_content_frame)
        # 画布布局
        self.canvas_content_layout = QGridLayout(self.canvas_content_frame)

    def setup_content(self):
        for index, origin_data_dict in enumerate(self.origin_data_dict_list):
            # 已删除的原数据字典名称
            origin_data_dict_label = QLabel()
            origin_data_dict_label.setObjectName('form_label')
            origin_data_dict_label.setText(origin_data_dict.dict_name)
            self.canvas_content_layout.addWidget(origin_data_dict_label, index, 0, 1, 1)
            # 箭头 label
            arrow_label = QLabel()
            arrow_label.setText(DATA_DICT_BIND_ARROW_TEXT)
            self.canvas_content_layout.addWidget(arrow_label, index, 1, 1, 1)
            # 新数据字典列表 combobox
            data_dict_combobox = QComboBox()
            self.canvas_content_layout.addWidget(data_dict_combobox, index, 2, 1, 1)
            data_dict_combobox.setPlaceholderText(DATA_DICT_COMBOBOX_PLACEHOLDER_TEXT)
            for data_dict in self.data_dict_list:
                data_dict_combobox.addItem(data_dict.dict_name, data_dict)
        # 添加一个空白label
        self.canvas_content_layout.addWidget(QLabel())

    def check_combobox_value(self):
        for row in range(self.canvas_content_layout.rowCount() - 1):
            combobox = self.canvas_content_layout.itemAtPosition(row, 2).widget()
            if combobox.currentIndex() == -1:
                return False
        return True

    def collect_data(self):
        for row in range(self.canvas_content_layout.rowCount() - 1):
            # 找到当前行原字典值
            origin_data_dict = self.origin_data_dict_list[row]
            # 找到指定的新字典值
            combobox = self.canvas_content_layout.itemAtPosition(row, 2).widget()
            index = combobox.currentIndex()
            new_data_dict = combobox.itemData(index)
            # 将原字典值绑定到新字典值下
            if not new_data_dict.bind_data_list:
                new_data_dict.bind_data_list = list()
            new_data_dict.bind_data_list.append(origin_data_dict)
