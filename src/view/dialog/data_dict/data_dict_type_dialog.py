# -*- coding: utf-8 -*-
from src.constant.data_dict_dialog_constant import DATA_DICT_TYPE_LIST_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.data_dict.data_dict_type_dialog_frame import DataDictTypeDialogFrame

_author_ = 'luwt'
_date_ = '2023/7/15 11:31'


class DataDictTypeDialog(CustomDialogABC):
    """数据字典类型对话框"""

    def __init__(self):
        super().__init__(DATA_DICT_TYPE_LIST_TITLE)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.4, self.window_geometry.height() >> 1)

    def get_frame(self) -> DataDictTypeDialogFrame:
        return DataDictTypeDialogFrame(self, self.dialog_title)
