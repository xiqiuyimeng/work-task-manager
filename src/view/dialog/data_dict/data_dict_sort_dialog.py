# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.constant.data_dict_dialog_constant import DATA_DICT_SORT_TITLE
from src.view.dialog.custom_dialog_abc import CustomSaveDialogABC
from src.view.frame.data_dict.data_dict_sort_dialog_frame import DataDictSortDialogFrame

_author_ = 'luwt'
_date_ = '2023/8/15 9:38'


class DataDictSortDialog(CustomSaveDialogABC):
    """数据字典排序对话框"""
    save_signal = pyqtSignal(list)

    def __init__(self, data_dict_list):
        self.data_dict_list = data_dict_list
        super().__init__(DATA_DICT_SORT_TITLE)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.4, self.window_geometry.height() >> 1)

    def get_frame(self) -> DataDictSortDialogFrame:
        return DataDictSortDialogFrame(self.data_dict_list, self, self.dialog_title)
