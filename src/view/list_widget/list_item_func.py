# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt

_author_ = 'luwt'
_date_ = '2023/8/15 10:04'


# 放入取出放置数据字典对象
def set_data_dict(item, data_dict):
    item.setData(Qt.ItemDataRole.UserRole, data_dict)


def get_data_dict(item):
    return item.data(Qt.ItemDataRole.UserRole)
