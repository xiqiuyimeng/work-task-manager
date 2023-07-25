# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel, QGridLayout

from src.constant.data_dict_dialog_constant import DATA_DICT_HEADER_TEXT, ORIGIN_DATA_DICT_HEADER_TEXT, \
    CHECK_COMBOBOX_PROMPT, CHECK_COMBOBOX_TITLE
from src.view.box.message_box import pop_fail
from src.view.frame.save_dialog_frame import SaveDialogFrame
from src.view.widget.data_dict_bind_widget import DataDictBindWidget

_author_ = 'luwt'
_date_ = '2023/7/24 16:55'


class DataDictBindDialogFrame(SaveDialogFrame):
    """被删除的数据字典值绑定的业务数据，转移到新数据字典值的对话框框架"""
    save_signal = pyqtSignal()

    def __init__(self, origin_data_dict_list, data_dict_list, *args):
        # 已删除且已绑定了数据的字典值列表
        self.origin_data_dict_list = origin_data_dict_list
        # 新的数据字典值列表
        self.data_dict_list = data_dict_list
        self.origin_data_dict_header_label: QLabel = ...
        self.data_dict_header_label: QLabel = ...
        self.header_layout: QGridLayout = ...
        self.content_widget: DataDictBindWidget = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        self.header_layout = QGridLayout()
        self.frame_layout.addLayout(self.header_layout)
        self.origin_data_dict_header_label = QLabel()
        self.origin_data_dict_header_label.setObjectName('form_label')
        self.header_layout.addWidget(self.origin_data_dict_header_label, 0, 0, 1, 1)
        self.header_layout.addWidget(QLabel(), 0, 1, 1, 1)
        self.data_dict_header_label = QLabel()
        self.data_dict_header_label.setObjectName('form_label')
        self.header_layout.addWidget(self.data_dict_header_label, 0, 2, 1, 1)

        self.content_widget = DataDictBindWidget(self.origin_data_dict_list, self.data_dict_list)
        self.content_widget.setup_content()
        self.frame_layout.addWidget(self.content_widget)

    def setup_other_label_text(self):
        self.origin_data_dict_header_label.setText(ORIGIN_DATA_DICT_HEADER_TEXT)
        self.data_dict_header_label.setText(DATA_DICT_HEADER_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        ...

    def save_func(self):
        if self.content_widget.check_combobox_value():
            # 收集数据，此时原数据已被修改，无需发送数据
            self.content_widget.collect_data()
            self.save_signal.emit()
            self.parent_dialog.close()
        else:
            pop_fail(CHECK_COMBOBOX_PROMPT, CHECK_COMBOBOX_TITLE, self.parent_dialog)

    # ------------------------------ 信号槽处理 end ------------------------------ #
