# -*- coding: utf-8 -*-
from PyQt6.QtGui import QAction

from src.constant.bar_constant import DATA_DICT_ACTION, DATA_DICT_ACTION_TIP, PROJECT_ACTION, PROJECT_ACTION_TIP, \
    EXIT_ACTION, EXIT_ACTION_TP, HELP_ACTION, HELP_ACTION_TIP, ABOUT_ACTION, ABOUT_ACTION_TIP
from src.enum.icon_enum import get_icon
from src.view.bar.bar_function import open_project_dialog, open_data_dict_dialog, open_help_dialog, open_about_dialog

_author_ = 'luwt'
_date_ = '2023/7/10 13:56'


def add_data_dict_action(main_window):
    data_dict_action = QAction(get_icon(DATA_DICT_ACTION), DATA_DICT_ACTION, main_window)
    data_dict_action.setStatusTip(DATA_DICT_ACTION_TIP)
    data_dict_action.triggered.connect(lambda: open_data_dict_dialog())
    return data_dict_action


def add_project_action(main_window):
    project_action = QAction(get_icon(PROJECT_ACTION), PROJECT_ACTION, main_window)
    project_action.setStatusTip(PROJECT_ACTION_TIP)
    project_action.triggered.connect(lambda: open_project_dialog())
    return project_action


def add_exit_action(main_window):
    exit_action = QAction(get_icon(EXIT_ACTION), EXIT_ACTION, main_window)
    exit_action.setStatusTip(EXIT_ACTION_TP)
    exit_action.triggered.connect(main_window.close)
    return exit_action


def add_help_action(main_window):
    help_action = QAction(get_icon(HELP_ACTION), HELP_ACTION, main_window)
    help_action.setStatusTip(HELP_ACTION_TIP)
    help_action.triggered.connect(lambda: open_help_dialog())
    return help_action


def add_about_action(main_window):
    about_action = QAction(get_icon(ABOUT_ACTION), ABOUT_ACTION, main_window)
    about_action.setStatusTip(ABOUT_ACTION_TIP)
    about_action.triggered.connect(lambda: open_about_dialog())
    return about_action
