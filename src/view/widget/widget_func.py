# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QComboBox, QFormLayout, QLineEdit

from src.service.util.data_dict_cache_util import get_data_dict_list
from src.service.util.project_cache_util import get_project_dict_list

_author_ = 'luwt'
_date_ = '2023/7/12 15:58'


def setup_grid_form_combox(layout, col, row=0):
    label = QLabel()
    label.setObjectName('form_label')
    combobox = QComboBox()
    form_layout = QFormLayout()
    form_layout.addRow(label, combobox)
    layout.addLayout(form_layout, row, col)
    return label, combobox


def setup_form_combox(layout):
    label = QLabel()
    label.setObjectName('form_label')
    combobox = QComboBox()
    layout.addRow(label, combobox)
    return label, combobox


def setup_form_lineedit(layout, col, row=0, lineedit_class=QLineEdit):
    label = QLabel()
    label.setObjectName('form_label')
    linedit = lineedit_class()
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


def fill_data_dict_combobox(combobox, data_dict_type_code):
    for data_dict in get_data_dict_list(data_dict_type_code):
        combobox.addItem(data_dict.dict_name, data_dict)


def update_data_dict_combobox(combobox, data_dict_type_code):
    # 记录原值
    origin_text = combobox.currentText()
    combobox.clear()
    fill_data_dict_combobox(combobox, data_dict_type_code)
    combobox.setCurrentText(origin_text)


def get_task_combobox_data(combobox, task, obj_property_name, id_property_name):
    index = combobox.currentIndex()
    if index >= 0:
        item_data = combobox.itemData(index)
        setattr(task, obj_property_name, item_data)
        setattr(task, id_property_name, item_data.id)
