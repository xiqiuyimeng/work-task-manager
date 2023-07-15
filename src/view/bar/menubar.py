# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QMenuBar, QMenu

from src.constant.bar_constant import FILE_MENU, HELP_MENU
from src.view.bar.bar_action import add_data_dict_action, add_project_action, add_exit_action, add_help_action, \
    add_about_action

_author_ = 'luwt'
_date_ = '2023/7/10 13:57'


class Menubar(QMenuBar):

    def __init__(self, window):
        super().__init__(window)
        self.main_window = window

        self.file_menu: QMenu = self.addMenu(FILE_MENU)
        self.help_menu = self.addMenu(HELP_MENU)

    def fill_menu_bar(self):
        # 数据字典
        self.add_data_dict_menu()
        # 项目
        self.add_project_menu()
        # 退出
        self.add_exit_menu()

        # 帮助
        self.add_help_menu()
        # 关于
        self.add_about_menu()

    def add_data_dict_menu(self):
        data_dict_action = add_data_dict_action(self.main_window)
        self.file_menu.addAction(data_dict_action)

    def add_project_menu(self):
        project_action = add_project_action(self.main_window)
        self.file_menu.addAction(project_action)

    def add_exit_menu(self):
        exit_action = add_exit_action(self.main_window)
        self.file_menu.addAction(exit_action)

    def add_help_menu(self):
        help_action = add_help_action(self.main_window)
        self.help_menu.addAction(help_action)

    def add_about_menu(self):
        about_action = add_about_action(self.main_window)
        self.help_menu.addAction(about_action)
