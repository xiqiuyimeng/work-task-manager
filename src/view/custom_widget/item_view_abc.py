# -*- coding: utf-8 -*-
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QAbstractItemView, QFrame, QMenu

from src.view.custom_widget.scrollable_widget import ScrollableWidget

_author_ = 'luwt'
_date_ = '2023/7/10 14:54'


class ItemViewABC(QAbstractItemView, ScrollableWidget):

    def __init__(self, parent):
        super().__init__(parent)
        # 设置无边框
        self.setFrameShape(QFrame.Shape.NoFrame)
        # 统一设置图标大小
        self.setIconSize(QSize(40, 30))

        self.connect_signal()

    def connect_signal(self):
        # 右击事件
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.handle_right_mouse_clicked)

    def handle_right_mouse_clicked(self, pos):
        # 获取当前元素，只有在元素上才显示菜单
        item = self.itemAt(pos)
        if item:
            # 生成右键菜单
            menu = QMenu()
            # 填充右键菜单内容
            self.fill_menu(item, menu)
            # 右键菜单点击事件
            menu.triggered.connect(self.right_menu_func)
            # 右键菜单弹出位置跟随焦点位置
            menu.exec(QCursor.pos())

    def fill_menu(self, item, menu):
        ...

    def right_menu_func(self, action):
        """
        点击右键菜单选项后触发事件
        :param action: 右键菜单中的选项
        """
        # 获取右键点击的项
        item = self.currentItem()
        action_text = action.text()
        self.do_right_menu_func(item, action_text)

    def do_right_menu_func(self, item, action_text):
        ...
