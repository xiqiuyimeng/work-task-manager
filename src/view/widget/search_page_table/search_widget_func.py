# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QComboBox, QFormLayout, QLineEdit

from src.service.util.data_dict_cache_util import get_data_dict_list
from src.service.util.project_cache_util import get_project_dict_list

_author_ = 'luwt'
_date_ = '2023/7/12 15:58'


def setup_form_combox(layout, col, row=0):
    label = QLabel()
    combobox = QComboBox()
    form_layout = QFormLayout()
    form_layout.addRow(label, combobox)
    layout.addLayout(form_layout, row, col)
    return label, combobox


def setup_form_lineedit(layout, col, row=0):
    label = QLabel()
    linedit = QLineEdit()
    form_layout = QFormLayout()
    form_layout.addRow(label, linedit)
    layout.addLayout(form_layout, row, col)
    return label, linedit


def fill_project_combobox(project_combobox):
    for project in get_project_dict_list():
        add_project_combobox_item(project_combobox, project)


def add_project_combobox_item(project_combobox, project):
    # 添加项目下拉框值
    project_combobox.addItem(project.project_name, project)


def update_project_combobox_item(project_combobox, project):
    # 更新项目下拉框值
    index = list(get_project_dict_list()).index(project)
    project_combobox.setItemText(index, project.project_name)
    project_combobox.setItemData(index, project, Qt.ItemDataRole.UserRole)


def fill_data_dict_combobox(combobox, data_dict_type):
    for data_dict in get_data_dict_list(data_dict_type):
        combobox.addItem(data_dict.dict_name)


def update_data_dict_combobox(combobox, data_dict_type):
    # 记录原值
    origin_text = combobox.currentText()
    combobox.clear()
    fill_data_dict_combobox(combobox, data_dict_type)
    combobox.setCurrentText(origin_text)
