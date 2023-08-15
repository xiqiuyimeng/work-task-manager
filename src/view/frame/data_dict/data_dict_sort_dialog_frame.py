# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.constant.help_constant import DATA_DICT_SORT_HELP
from src.view.frame.save_dialog_frame import SaveDialogFrame
from src.view.list_widget.data_dict_list_widget import DataDictSortListWidget

_author_ = 'luwt'
_date_ = '2023/8/15 9:38'


class DataDictSortDialogFrame(SaveDialogFrame):
    """数据字典排序对话框框架"""
    save_signal = pyqtSignal(list)

    def __init__(self, data_dict_list, *args):
        self.data_dict_list = data_dict_list
        self.list_widget: DataDictSortListWidget = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        self.list_widget = DataDictSortListWidget(self)
        self.frame_layout.addWidget(self.list_widget)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        return DATA_DICT_SORT_HELP

    def save_func(self):
        data_dict_list = self.list_widget.collect_data_dict_list()
        self.save_signal.emit(data_dict_list)
        self.parent_dialog.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        super().post_process()
        self.list_widget.fill_list_widget(self.data_dict_list)

    # ------------------------------ 后置处理 end ------------------------------ #
