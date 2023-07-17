# -*- coding: utf-8 -*-
from src.constant.help_constant import CENTRAL_HELP
from src.view.dialog.about_dialog import AboutDialog
from src.view.dialog.data_dict.data_dict_type_dialog import DataDictTypeDialog
from src.view.dialog.help_dialog import HelpDialog

_author_ = 'luwt'
_date_ = '2023/7/10 14:02'


def open_data_dict_dialog():
    """打开数据字典管理对话框"""
    DataDictTypeDialog().exec()


def open_project_dialog():
    """打开项目管理对话框"""
    ...


def open_help_dialog():
    """打开帮助信息对话框"""
    HelpDialog(CENTRAL_HELP).exec()


def open_about_dialog():
    """打开关于信息对话框"""
    AboutDialog().exec()
