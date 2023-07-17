# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QLabel, QComboBox, QFormLayout, QLineEdit

from src.service.util.data_dict_cache_util import get_data_dict

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


def fill_data_dict_combobox(combobox, data_dict_type):
    for data_dict in get_data_dict(data_dict_type):
        combobox.addItem(data_dict.dict_name)
    combobox.setCurrentIndex(-1)


def update_data_dict_combobox(combobox, data_dict_type):
    combobox.clear()
    fill_data_dict_combobox(combobox, data_dict_type)
