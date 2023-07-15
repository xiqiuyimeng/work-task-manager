# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QStackedWidget

from src.constant.dialog_constant import NAME_UNCHANGED_PROMPT, NAME_AVAILABLE, NAME_EXISTS
from src.service.read_qrc.read_config import read_qss

_author_ = 'luwt'
_date_ = '2023/7/10 14:58'


def set_name_input_style(name_available: bool, current_name: str, old_name: str,
                         name_input_qss_id: str, name_input: QLineEdit, name_checker: QLabel):
    if name_available:
        # 如果名称无变化，提示
        if old_name == current_name:
            prompt = NAME_UNCHANGED_PROMPT
        else:
            prompt = NAME_AVAILABLE.format(current_name)
        style = "color:green"
        # 重载样式表
        name_input.setStyleSheet(read_qss())
    else:
        prompt = NAME_EXISTS.format(current_name)
        style = "color:red"
        name_input.setStyleSheet(f"#{name_input_qss_id}{{border-color:red;color:red}}")
    name_checker.setText(prompt)
    name_checker.setStyleSheet(style)


def reset_name_input_style(name_input: QLineEdit, name_checker: QLabel):
    name_input.setStyleSheet(read_qss())
    name_checker.setStyleSheet(read_qss())
    name_checker.setText('')


def check_available(name, old_name, exits_names):
    if old_name:
        # 假如原有的名称已经重复，那么再输入一遍原有名称，应该提示不可用
        if exits_names.count(old_name) > 1 and name == old_name:
            return False
        return (old_name != name and name not in exits_names) or old_name == name
    else:
        return name not in exits_names


def check_name_available(name, old_name, exits_names, name_input, name_checker, name_input_qss_id):
    if name:
        name_available = check_available(name, old_name, exits_names)
        set_name_input_style(name_available, name, old_name, name_input_qss_id, name_input, name_checker)
        return name_available
    else:
        reset_name_input_style(name_input, name_checker)
        return False


# ---------------------------------------- 构造左边列表，右边堆栈式窗口布局 ---------------------------------------- #

def construct_list_stacked_ui(list_widget_type: type, frame_layout: QVBoxLayout,
                              parent_frame: QFrame, left_stretch, right_stretch):
    # 创建布局，放置列表部件和堆栈式窗口部件
    parent_frame.stacked_layout = QHBoxLayout(parent_frame)
    frame_layout.addLayout(parent_frame.stacked_layout)
    # 创建列表部件
    parent_frame.list_widget = list_widget_type(parent_frame)
    parent_frame.stacked_layout.addWidget(parent_frame.list_widget)
    # 创建堆栈式窗口
    parent_frame.stacked_widget = QStackedWidget(parent_frame)
    parent_frame.stacked_layout.addWidget(parent_frame.stacked_widget)
    # 设置左右比例
    parent_frame.stacked_layout.setStretch(0, left_stretch)
    parent_frame.stacked_layout.setStretch(1, right_stretch)

    # 连接信号
    parent_frame.list_widget.currentRowChanged.connect(parent_frame.stacked_widget.setCurrentIndex)