# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QLabel, QComboBox, QFormLayout, QLineEdit

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
