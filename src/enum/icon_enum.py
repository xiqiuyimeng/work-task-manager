# -*- coding: utf-8 -*-
from enum import Enum

from PyQt6.QtGui import QIcon

from src.constant.bar_constant import DATA_DICT_ACTION, PROJECT_ACTION, EXIT_ACTION, HELP_ACTION, ABOUT_ACTION
from src.constant.table_constant import ROW_OPERATION_ICON, ROW_CAT_EDIT_ICON, ROW_DEL_ICON

_author_ = 'luwt'
_date_ = '2023/7/10 13:59'


icon_dict = dict()


class IconEnum(Enum):

    # window icon
    window_icon = 'window', 'icon:add.png'

    # bar icon
    data_dict_icon = DATA_DICT_ACTION, 'icon:table_icon.png'
    project_icon = PROJECT_ACTION, 'icon:template.png'
    exit_icon = EXIT_ACTION, 'icon:exit.png'
    help_icon = HELP_ACTION, 'icon:exec.png'
    about_icon = ABOUT_ACTION, 'icon:exec.png'

    # 通用表格最后一列操作 icon
    row_operation_icon = ROW_OPERATION_ICON, 'icon:right.png'
    row_cat_edit_icon = ROW_CAT_EDIT_ICON, 'icon:exec.png'
    row_del_icon = ROW_DEL_ICON, 'icon:remove.png'


def get_icon_path(name):
    for icon_enum in IconEnum:
        if icon_enum.value[0] == name:
            return icon_enum.value[1]
    # 如果获取不到，给个默认值，创建一个空icon对象，避免程序出错
    return 'default_icon_path'


def create_icon(icon_path, name):
    icon = QIcon(icon_path)
    icon_dict[icon_path] = icon
    return get_icon(name)


def get_icon(name):
    icon_path = get_icon_path(name)
    if icon_path:
        # 首先获取icon，如果不存在，再创建icon
        icon = icon_dict.get(icon_path)
        if not icon:
            return create_icon(icon_path, name)
        return icon
