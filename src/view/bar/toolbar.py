# -*- coding: utf-8 -*-
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QToolBar

from src.view.bar.bar_action import add_help_action, add_about_action, add_exit_action
from src.view.custom_widget.draggable_widget import DraggableWidget

_author_ = 'luwt'
_date_ = '2023/7/10 13:54'


class ToolBar(QToolBar, DraggableWidget):

    def __init__(self, window):
        super().__init__(window)
        self.main_window = window
        self.setObjectName("toolbar")

        self.setIconSize(QSize(50, 40))
        # 设置名称显示在图标下面（默认本来是只显示图标）
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

    def fill_tool_bar(self):
        # 帮助
        self.add_help_tool()
        # 关于
        self.add_about_tool()
        # 退出
        self.add_exit_tool()

    def add_help_tool(self):
        help_tool = add_help_action(self.main_window)
        self.addAction(help_tool)

    def add_about_tool(self):
        about_tool = add_about_action(self.main_window)
        self.addAction(about_tool)

    def add_exit_tool(self):
        exit_tool = add_exit_action(self.main_window)
        self.addAction(exit_tool)
