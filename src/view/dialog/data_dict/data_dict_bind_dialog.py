# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.constant.data_dict_dialog_constant import MAINTAIN_DATA_DICT_BIND_TITLE
from src.view.dialog.custom_dialog_abc import CustomSaveDialogABC
from src.view.frame.data_dict.data_dict_bind_dialog_frame import DataDictBindDialogFrame

_author_ = 'luwt'
_date_ = '2023/7/25 11:10'


class DataDictBindDialog(CustomSaveDialogABC):
    """被删除的数据字典值绑定的业务数据，转移到新数据字典值的对话框"""
    save_signal = pyqtSignal()

    def __init__(self, origin_data_dict_list, data_dict_list):
        self.origin_data_dict_list = origin_data_dict_list
        self.data_dict_list = data_dict_list
        super().__init__(MAINTAIN_DATA_DICT_BIND_TITLE)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.5, self.window_geometry.height() * 0.6)

    def get_frame(self) -> DataDictBindDialogFrame:
        return DataDictBindDialogFrame(self.origin_data_dict_list, self.data_dict_list, self, self.dialog_title)
