# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QButtonGroup, QComboBox

from src.constant.page_constant import TOTAL_COUNT_LABEL_TEXT, PAGE_SIZE_LABEL_TEXT, JUMP_PAGE_LEFT_LABEL_TEXT, \
    JUMP_PAGE_RIGHT_LABEL_TEXT, PAGE_SIZE_RANGE, FIRST_PAGE_BUTTON_TEXT, PREVIOUS_PAGE_BUTTON_TEXT, \
    NEXT_PAGE_BUTTON_TEXT, LAST_PAGE_BUTTON_TEXT, MORE_PAGE_BUTTON_TEXT, MORE_PAGE_RIGHT_BUTTON_TEXT, \
    MORE_PAGE_LEFT_BUTTON_TEXT
from src.service.read_qrc.read_config import read_qss
from src.service.util.page_util import Page
from src.view.custom_widget.page.page_component import PageLineEdit, PageButton

_author_ = 'luwt'
_date_ = '2023/7/12 9:58'


def adjust_label_width(label: QLabel):
    text_width = label.fontMetrics().boundingRect(label.text()).width()
    label.setFixedWidth(text_width)


def adjust_button_width(button: QPushButton):
    text_width = button.fontMetrics().boundingRect(button.text()).width()
    button.setFixedWidth(text_width + 30)


class PageWidget(QWidget):
    """分页控件"""
    page_changed = pyqtSignal(Page)

    def __init__(self):
        # 分页数据
        self.page_data: Page = ...
        self._layout: QHBoxLayout = ...
        # 总条数
        self.total_count_label: QLabel = ...
        # 每页条数
        self.page_size_combobox: QComboBox = ...
        self.page_size_label: QLabel = ...
        # 跳转页码
        self.jump_page_left_label: QLabel = ...
        self.jump_page_lineedit: PageLineEdit = ...
        self.jump_page_right_label: QLabel = ...
        # 首页
        self.first_page_button: PageButton = ...
        # 上一页
        self.previous_page_button: PageButton = ...
        # 按钮组
        self.button_group: QButtonGroup = ...
        self.group_first_button: PageButton = ...
        self.group_second_button: PageButton = ...
        self.group_third_button: PageButton = ...
        self.group_forth_button: PageButton = ...
        self.group_fifth_button: PageButton = ...
        self.group_sixth_button: PageButton = ...
        self.group_seventh_button: PageButton = ...
        self.origin_current_button: PageButton = ...
        # 下一页
        self.next_page_button: PageButton = ...
        # 最后一页
        self.last_page_button: PageButton = ...
        super().__init__()

        self.setup_ui()
        self.setup_label_text()
        self.connect_signal()
        self.installEventFilter(self.jump_page_lineedit)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_ui(self):
        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        # 左侧增加一个占位label
        self._layout.addWidget(QLabel())

        # 总条数
        self.total_count_label = QLabel()
        self._layout.addWidget(self.total_count_label)
        self._layout.addSpacing(20)

        # 每页条数
        self.page_size_combobox = QComboBox()
        self._layout.addWidget(self.page_size_combobox)
        self.page_size_label = QLabel()
        self._layout.addWidget(self.page_size_label)
        self._layout.addSpacing(20)

        # 跳转页码
        self.jump_page_left_label = QLabel()
        self._layout.addWidget(self.jump_page_left_label)
        self.jump_page_lineedit = PageLineEdit()
        self._layout.addWidget(self.jump_page_lineedit)
        self.jump_page_right_label = QLabel()
        self._layout.addWidget(self.jump_page_right_label)

        # 首页按钮
        self.first_page_button = PageButton()
        self.first_page_button.setObjectName('first_last_page_button')
        self._layout.addWidget(self.first_page_button)

        # 上一页按钮
        self.previous_page_button = PageButton()
        self.previous_page_button.setObjectName('previous_next_page_button')
        self._layout.addWidget(self.previous_page_button)

        # 跳转页码按钮组
        self.button_group = QButtonGroup()
        self.group_first_button = self.setup_group_button()
        self.group_second_button = self.setup_group_button()
        self.group_third_button = self.setup_group_button()
        self.group_forth_button = self.setup_group_button()
        self.group_fifth_button = self.setup_group_button()
        self.group_sixth_button = self.setup_group_button()
        self.group_seventh_button = self.setup_group_button()

        # 下一页按钮
        self.next_page_button = PageButton()
        self.next_page_button.setObjectName('previous_next_page_button')
        self._layout.addWidget(self.next_page_button)

        # 尾页按钮
        self.last_page_button = PageButton()
        self.last_page_button.setObjectName('first_last_page_button')
        self._layout.addWidget(self.last_page_button)

    def setup_group_button(self):
        button = PageButton()
        button.setObjectName('jump_page_button')
        self._layout.addWidget(button)
        self.button_group.addButton(button)
        return button

    def setup_label_text(self):
        self.page_size_label.setText(PAGE_SIZE_LABEL_TEXT)
        self.jump_page_left_label.setText(JUMP_PAGE_LEFT_LABEL_TEXT)
        self.jump_page_right_label.setText(JUMP_PAGE_RIGHT_LABEL_TEXT)
        self.page_size_combobox.addItems(PAGE_SIZE_RANGE)
        self.first_page_button.setText(FIRST_PAGE_BUTTON_TEXT)
        self.previous_page_button.setText(PREVIOUS_PAGE_BUTTON_TEXT)
        self.next_page_button.setText(NEXT_PAGE_BUTTON_TEXT)
        self.last_page_button.setText(LAST_PAGE_BUTTON_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_signal(self):
        self.page_size_combobox.currentIndexChanged.connect(self.page_size_changed)
        self.jump_page_lineedit.text_edit_changed.connect(self.jump_page)
        self.first_page_button.clicked.connect(self.first_button_clicked)
        self.previous_page_button.clicked.connect(self.previous_button_clicked)
        self.button_group.buttonClicked.connect(self.button_group_clicked)
        self.next_page_button.clicked.connect(self.next_button_clicked)
        self.last_page_button.clicked.connect(self.last_button_clicked)

    def page_size_changed(self):
        self.page_data.page_size = int(self.page_size_combobox.currentText())
        # 当页条数发生变化，触发信号
        self.page_changed.emit(self.page_data)

    def jump_page(self):
        text = self.jump_page_lineedit.text()
        self.page_data.page_no = int(text)

        # 如果当前页是第一页，那么上一页、首页按钮不可用
        first_page_flag = text == self.group_first_button.text()
        self.previous_page_button.setDisabled(first_page_flag)
        self.first_page_button.setDisabled(first_page_flag)
        # 如果总页数等于当前页，那么下一页、尾页按钮不可用
        last_page_flag = text == str(self.page_data.total_page)
        self.next_page_button.setDisabled(last_page_flag)
        self.last_page_button.setDisabled(last_page_flag)

        self.set_current_page_button()
        # 页码发生变化，触发信号
        self.page_changed.emit(self.page_data)

    def set_current_page_button(self):
        # 渲染按钮组
        if self.page_data.total_page > len(self.button_group.buttons()):
            self.dynamic_render_more_page_button_group()
        # 按钮组
        for button in self.button_group.buttons():
            if button.text() == str(self.page_data.page_no):
                if self.origin_current_button is not Ellipsis:
                    self.origin_current_button.setDisabled(False)
                    self.origin_current_button.setObjectName('jump_page_button')
                    self.origin_current_button.setStyleSheet(read_qss())
                self.origin_current_button = button
                button.setObjectName('current_page_button')
                button.setStyleSheet(read_qss())
                button.setDisabled(True)

    def dynamic_render_more_page_button_group(self):
        # 设置所有按钮都显示
        for button in self.button_group.buttons():
            button.show()
        # 清空省略号属性
        self.group_second_button.set_more_page_left_button(False)
        self.group_sixth_button.set_more_page_right_button(False)

        # 对于第一个按钮和最后一个按钮，直接赋值
        self.group_first_button.setText('1')
        self.group_seventh_button.setText(str(self.page_data.total_page))

        # 如果当前页小于等于4，第六个按钮为省略号：1 2 3 4 5 ... total
        if self.page_data.page_no <= 4:
            for idx in range(2, 6):
                button = self.button_group.buttons()[idx - 1]
                button.setText(str(idx))
            self.group_sixth_button.setText(MORE_PAGE_BUTTON_TEXT)
            self.group_sixth_button.set_more_page_right_button(True)
        elif self.page_data.page_no > 4:
            # 如果当前页大于 4 且当前页 + 3 小于总页数，第二个按钮置为省略号，第六个按钮为省略号
            # 1 ... current-1 current current+1 ... total
            if self.page_data.page_no + 3 < self.page_data.total_page:
                self.group_second_button.setText(MORE_PAGE_BUTTON_TEXT)
                self.group_second_button.set_more_page_left_button(True)
                self.group_sixth_button.setText(MORE_PAGE_BUTTON_TEXT)
                self.group_sixth_button.set_more_page_right_button(True)
                self.group_third_button.setText(str(self.page_data.page_no - 1))
                self.group_forth_button.setText(str(self.page_data.page_no))
                self.group_fifth_button.setText(str(self.page_data.page_no + 1))
            else:
                # 如果当前页大于 4 且当前页 + 3 大于等于总页数，第二个按钮置为省略号，第三个按钮到最后一个按钮分别为
                # 总页数 -4 到总页数 -1  1 ... total-4 total-3 total-2 total-1 total
                self.group_second_button.setText(MORE_PAGE_BUTTON_TEXT)
                self.group_second_button.set_more_page_left_button(True)
                for idx in range(2, 6):
                    button = self.button_group.buttons()[idx]
                    button.setText(str(self.page_data.total_page - 6 + idx))

    def first_button_clicked(self):
        self.jump_page_lineedit.init_page()
        self.jump_page()

    def previous_button_clicked(self):
        self.page_data.page_no = max(int(self.group_first_button.text()), self.page_data.page_no - 1)
        self.set_current_page_no()
        self.jump_page()

    def button_group_clicked(self, button):
        text = button.text()
        if text == MORE_PAGE_LEFT_BUTTON_TEXT:
            self.page_data.page_no = max(int(self.group_first_button.text()), self.page_data.page_no - 3)
        elif text == MORE_PAGE_RIGHT_BUTTON_TEXT:
            self.page_data.page_no = min(self.page_data.total_page, self.page_data.page_no + 3)
        else:
            self.page_data.page_no = int(text)
        self.set_current_page_no()
        self.jump_page()

    def set_current_page_no(self):
        # 跳转页码
        self.jump_page_lineedit.setText(str(self.page_data.page_no))

    def next_button_clicked(self):
        self.page_data.page_no = min(self.page_data.total_page, self.page_data.page_no + 1)
        self.set_current_page_no()
        self.jump_page()

    def last_button_clicked(self):
        self.jump_page_lineedit.setText(str(self.page_data.total_page))
        self.jump_page()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    def init_page_data(self):
        self.page_data = Page().init_page()
        self.update_page()

    def update_page(self):
        self.blockSignals(True)
        self.page_size_combobox.setCurrentIndex(PAGE_SIZE_RANGE.index(str(self.page_data.page_size)))
        self.total_count_label.setText(TOTAL_COUNT_LABEL_TEXT.format(self.page_data.total_count))

        # 动态渲染按钮组
        self.dynamic_render_button_group()

        # 给PageLineEdit设置初始页码
        self.jump_page_lineedit.set_init_page_no(self.group_first_button.text())
        # 设置最大页码
        self.jump_page_lineedit.set_max_page_no(self.page_data.total_page)
        self.jump_page_lineedit.set_current_page(self.page_data.page_no)
        self.jump_page()
        self.blockSignals(False)

        # 调整控件尺寸
        self.adjust_widget_size()

    def dynamic_render_button_group(self):
        # 跳转页码按钮组，根据当前总页数动态渲染
        if self.page_data.total_page <= len(self.button_group.buttons()):
            # 如果总页数不大于按钮组的按钮数，那么按实际页数渲染
            for idx, button in enumerate(self.button_group.buttons(), start=1):
                if idx <= self.page_data.total_page:
                    button.setText(str(idx))
                    button.show()
                else:
                    button.hide()
        else:
            self.dynamic_render_more_page_button_group()

    def adjust_widget_size(self):
        # 设置每个控件尺寸大小
        adjust_label_width(self.total_count_label)
        self.page_size_combobox.setMaximumWidth(50)
        adjust_label_width(self.page_size_label)
        adjust_label_width(self.jump_page_left_label)
        self.jump_page_lineedit.setMaximumWidth(50)
        adjust_label_width(self.jump_page_right_label)

        adjust_button_width(self.first_page_button)
        adjust_button_width(self.previous_page_button)
        # 按钮组
        for button in self.button_group.buttons():
            adjust_button_width(button)
        adjust_button_width(self.next_page_button)
        adjust_button_width(self.last_page_button)
