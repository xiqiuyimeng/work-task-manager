# -*- coding: utf-8 -*-
from src.constant.data_dict_dialog_constant import DATA_DICT_DETAIL_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.data_dict.data_dict_detail_dialog_frame import DataDictDetailDialogFrame

_author_ = 'luwt'
_date_ = '2023/7/15 12:03'


class DataDictDetailDialog(CustomDialogABC):
    """数据字典详情对话框"""

    def __init__(self, data_dict_type):
        self.data_dict_type = data_dict_type
        super().__init__(DATA_DICT_DETAIL_TITLE.format(data_dict_type[1]))

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.5, self.window_geometry.height() * 0.6)

    def get_frame(self) -> DataDictDetailDialogFrame:
        return DataDictDetailDialogFrame(self.data_dict_type, self, self.dialog_title)
