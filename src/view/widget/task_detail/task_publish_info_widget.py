# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QFrame, QCheckBox, QComboBox

from src.constant.task_constant import ADD_PUBLISH_INFO_BUTTON_TEXT, DELETE_PUBLISH_INFO_BUTTON_TEXT
from src.enum.data_dict_enum import DataDictTypeEnum
from src.service.system_storage.publish_info_sqlite import PublishInfo
from src.view.custom_widget.scrollable_widget import ScrollArea
from src.view.custom_widget.text_editor import TextEditor
from src.view.widget.widget_func import fill_data_dict_combobox, get_combobox_data, clear_gridlayout

_author_ = 'luwt'
_date_ = '2023/8/15 14:57'


class TaskPublishInfoWidget(QWidget):

    def __init__(self):
        self.publish_info_list = list()
        self.check_box_list = list()
        self._layout: QVBoxLayout = ...
        # 按钮区
        self.button_layout: QGridLayout = ...
        # 添加按钮
        self.add_button: QPushButton = ...
        # 删除按钮
        self.delete_button: QPushButton = ...
        # 内容区
        self.scroll_area: ScrollArea = ...
        self.content_frame: QFrame = ...
        self.content_layout: QGridLayout = ...
        # 默认行索引
        self.content_row = 0
        super().__init__()

    def setup_ui(self):
        self._layout = QVBoxLayout(self)
        self.button_layout = QGridLayout(self)
        self._layout.addLayout(self.button_layout)

        self.button_layout.addWidget(QLabel(), 0, 0, 1, 3)
        self.add_button = QPushButton()
        self.add_button.setObjectName('add_button')
        self.button_layout.addWidget(self.add_button, 0, 3, 1, 1)
        self.delete_button = QPushButton()
        self.delete_button.setObjectName('del_button')
        self.button_layout.addWidget(self.delete_button, 0, 4, 1, 1)

        self.scroll_area = ScrollArea()
        self._layout.addWidget(self.scroll_area)
        self.content_frame = QFrame()
        self.scroll_area.set_canvas_widget(self.content_frame)
        self.content_layout = QGridLayout(self.content_frame)

    def setup_label_text(self):
        self.add_button.setText(ADD_PUBLISH_INFO_BUTTON_TEXT)
        self.delete_button.setText(DELETE_PUBLISH_INFO_BUTTON_TEXT)

    def collect_data(self, task):
        # 收集之前先清空容器
        self.publish_info_list.clear()
        self.do_collect_data()
        task.publish_info_list = self.publish_info_list

    def do_collect_data(self, check_state=None):
        for row in range(self.content_row):
            combobox_layout = self.content_layout.itemAtPosition(row, 0)
            check_box = combobox_layout.itemAtPosition(0, 0).widget()
            # 如果存在筛选，但条件不符合，跳过
            if check_state is not None and check_state != check_box.checkState():
                continue
            combobox = combobox_layout.itemAtPosition(0, 1).widget()
            # 创建发版信息对象
            publish_info = PublishInfo()
            self.publish_info_list.append(publish_info)
            get_combobox_data(combobox, publish_info, 'publish_type_id', 'publish_type')
            text_editor = self.content_layout.itemAtPosition(row, 1).widget()
            publish_info.publish_info = text_editor.toPlainText()

    def echo_data(self, task):
        self.publish_info_list = task.publish_info_list
        self.do_echo_data()

    def do_echo_data(self):
        for publish_info in self.publish_info_list:
            self.add_publish_info(publish_info)

    def connect_signal(self):
        self.add_button.clicked.connect(self.add_publish_info)
        self.delete_button.clicked.connect(self.del_publish_info)

    def add_publish_info(self, publish_info=None):
        layout = QGridLayout()
        self.content_layout.addLayout(layout, self.content_row, 0, 1, 1)
        check_box = QCheckBox()
        self.check_box_list.append(check_box)
        layout.addWidget(check_box, 0, 0, 1, 1)
        combobox = QComboBox()
        fill_data_dict_combobox(combobox, DataDictTypeEnum.publish_type.value[0])
        layout.addWidget(combobox, 0, 1, 1, 1)
        layout.addWidget(QLabel(), 1, 0, 1, 2)
        text_editor = TextEditor()
        text_editor.setFixedHeight(150)
        self.content_layout.addWidget(text_editor, self.content_row, 1, 1, 5)
        # 行数 +1
        self.content_row += 1
        # 数据回显
        if publish_info:
            combobox.setCurrentText(publish_info.publish_type.dict_name)
            text_editor.setPlainText(publish_info.publish_info)

    def del_publish_info(self):
        self.publish_info_list.clear()
        # 收集未选中的数据
        self.do_collect_data(Qt.CheckState.Unchecked)
        # 清空布局
        clear_gridlayout(self.content_layout)
        self.content_row = 0
        # 重新渲染回显数据
        self.do_echo_data()
        self.publish_info_list.clear()
