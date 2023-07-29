# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeyEvent, QIntValidator
from PyQt6.QtWidgets import QLineEdit, QPushButton

from src.constant.page_constant import MORE_PAGE_LEFT_BUTTON_TEXT, MORE_PAGE_RIGHT_BUTTON_TEXT

_author_ = 'luwt'
_date_ = '2023/7/13 17:04'


class PageButton(QPushButton):

    def __init__(self):
        self.more_page_right_button = False
        self.more_page_left_button = False
        self.origin_text = ...
        self.enter_button = False
        super().__init__()

    def set_more_page_right_button(self, more_page):
        self.more_page_right_button = more_page

    def set_more_page_left_button(self, more_page):
        self.more_page_left_button = more_page

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.set_more_button_text()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.set_more_button_text()

    def enterEvent(self, event):
        if self.isEnabled():
            self.enter_button = True
        super().enterEvent(event)
        self.set_more_button_text()

    def set_more_button_text(self):
        if self.more_page_left_button:
            self.origin_text = self.text()
            self.setText(MORE_PAGE_LEFT_BUTTON_TEXT)
        elif self.more_page_right_button:
            self.origin_text = self.text()
            self.setText(MORE_PAGE_RIGHT_BUTTON_TEXT)

    def leaveEvent(self, event):
        self.enter_button = False
        super().leaveEvent(event)
        if self.more_page_right_button or self.more_page_left_button:
            # 离开需要重置文本
            self.setText(self.origin_text)


class PageLineEdit(QLineEdit):
    text_edit_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setValidator(QIntValidator())
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.init_page_no = ...
        self.max_page_no = ...
        self.page_button_list = ...

    def set_init_page_no(self, page_no):
        self.init_page_no = page_no

    def init_page(self):
        self.setText(self.init_page_no)

    def set_current_page(self, page_no):
        self.setText(str(page_no))

    def set_max_page_no(self, page_no):
        self.max_page_no = page_no

    def text_edit_complete(self):
        # 窗口活动时，再处理
        if not self.window().isActiveWindow():
            return
        # 如果值非法，那么重置
        if not self.text() or int(self.text()) < 1:
            self.init_page()
        # 如果大于最大页数，那么重置为最大页数
        elif int(self.text()) > self.max_page_no:
            self.setText(str(self.max_page_no))
        self.text_edit_changed.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        if self.page_button_list is Ellipsis:
            parent_layout = self.parent().layout()
            self.page_button_list = list()
            for idx in range(parent_layout.count()):
                button = parent_layout.itemAt(idx).widget()
                if isinstance(button, PageButton):
                    self.page_button_list.append(button)
        # 如果现在已经进入了某个分页按钮，这时释焦，那么下一个动作必然是点击按钮，
        # 为避免两次触发page数据变化，所以禁止发信号
        if not any([button.enter_button for button in self.page_button_list]):
            self.text_edit_complete()

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.text_edit_complete()
