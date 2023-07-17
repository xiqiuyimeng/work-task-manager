# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QLabel

from src.constant.data_dict_dialog_constant import DATA_DICT_TYPE_OPERATION_TIP
from src.enum.data_dict_enum import get_data_dict_type_names, get_data_dict_type_by_name
from src.view.dialog.data_dict.data_dict_detail_dialog import DataDictDetailDialog
from src.view.frame.dialog_frame_abc import DialogFrameABC
from src.view.list_widget.data_dict_list_widget import DataDictListWidget

_author_ = 'luwt'
_date_ = '2023/7/15 11:31'


class DataDictTypeDialogFrame(DialogFrameABC):
    """数据字典类型对话框框架"""

    def __init__(self, *args):
        # 操作提示
        self.operation_tip_label: QLabel = ...
        # 数据字典列表控件
        self.data_dict_list_widget: DataDictListWidget = ...
        # 详情对话框
        self.data_dict_detail_dialog: DataDictDetailDialog = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #
    def setup_content_ui(self):
        self.operation_tip_label = QLabel()
        self.operation_tip_label.setObjectName('tips_label')
        self.frame_layout.addWidget(self.operation_tip_label)

        self.data_dict_list_widget = DataDictListWidget(self.open_data_dict_detail_dialog, self)
        self.frame_layout.addWidget(self.data_dict_list_widget)

    def setup_other_label_text(self):
        self.operation_tip_label.setText(DATA_DICT_TYPE_OPERATION_TIP)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        ...

    def open_data_dict_detail_dialog(self, data_dict_type_name):
        data_dict_type = get_data_dict_type_by_name(data_dict_type_name)
        self.data_dict_detail_dialog = DataDictDetailDialog(data_dict_type)
        self.data_dict_detail_dialog.exec()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        self.data_dict_list_widget.fill_list_widget(get_data_dict_type_names())

    # ------------------------------ 后置处理 end ------------------------------ #
