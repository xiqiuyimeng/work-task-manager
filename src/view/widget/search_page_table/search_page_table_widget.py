# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel

from src.constant.window_constant import RESET_SEARCH_BTN_TEXT, SEARCH_BTN_TEXT, DEL_BTN_TEXT
from src.service.async_func.async_task_abc import LoadingMaskThreadExecutor
from src.view.custom_widget.page_widget import PageWidget
from src.view.table.table_widget.custom_table_widget import CustomTableWidget

_author_ = 'luwt'
_date_ = '2023/7/12 10:03'


class SearchPageTableWidget(QWidget):
    """包含搜索区、表格数据区、分页组件的部件"""

    def __init__(self):
        # 主布局
        self._layout: QVBoxLayout = ...
        # 搜索框布局
        self.search_layout: QGridLayout = ...
        # 按钮布局
        self.button_layout: QGridLayout = ...
        # 重置、查询、删除按钮
        self.reset_search_button: QPushButton = ...
        self.search_button: QPushButton = ...
        self.del_button: QPushButton = ...
        # 数据表格
        self.table_widget: CustomTableWidget = ...
        # 分页组件
        self.page_widget: PageWidget = ...
        # 搜索数据列表执行器
        self.search_executor: LoadingMaskThreadExecutor = ...
        super().__init__()

        self.setup_ui()
        self.setup_label_text()
        self.connect_signal()
        self.post_process()

    def setup_ui(self):
        self._layout = QVBoxLayout(self)

        # 创建搜索区域
        self.setup_search_ui()

        self.button_layout = QGridLayout(self)
        self._layout.addLayout(self.button_layout)
        # 创建按钮区
        self.setup_button_ui()

        # 主数据表格
        self.table_widget = self.get_table_widget()
        self._layout.addWidget(self.table_widget)

        # 分页组件
        self.page_widget = PageWidget()
        self._layout.addWidget(self.page_widget)

    def setup_search_ui(self):
        ...

    def setup_button_ui(self, blank_left=8):
        self.del_button = QPushButton()
        self.del_button.setObjectName('del_button')
        self.button_layout.addWidget(self.del_button, 0, 0, 1, 1)
        self.button_layout.addWidget(QLabel(), 0, 1, 1, blank_left)
        self.reset_search_button = QPushButton()
        self.reset_search_button.setObjectName('reset_search_button')
        self.button_layout.addWidget(self.reset_search_button, 0, blank_left + 1, 1, 1)
        self.search_button = QPushButton()
        self.search_button.setObjectName('search_button')
        self.button_layout.addWidget(self.search_button, 0, blank_left + 2, 1, 1)

    def get_table_widget(self) -> CustomTableWidget:
        ...

    def setup_label_text(self):
        self.reset_search_button.setText(RESET_SEARCH_BTN_TEXT)
        self.search_button.setText(SEARCH_BTN_TEXT)
        self.del_button.setText(DEL_BTN_TEXT)
        self.setup_search_label_text()

    def setup_search_label_text(self):
        ...

    def connect_signal(self):
        self.reset_search_button.clicked.connect(self.reset_search)
        self.search_button.clicked.connect(self.search)
        self.del_button.clicked.connect(self.del_rows)
        # 表格表头选中状态变化
        self.table_widget.header_widget.header_check_changed.connect(self.set_button_available)

    def reset_search(self):
        # 清空数据
        self.reset_search_data()
        # 重新搜索
        self.search()

    def reset_search_data(self):
        ...

    def search(self):
        self.search_executor = self.get_search_executor()
        # 添加搜索条件
        self.search_executor.start()

    def get_search_executor(self) -> LoadingMaskThreadExecutor:
        ...

    def del_rows(self):
        ...

    def set_button_available(self, checked):
        # 如果表格存在行，删除按钮状态根据传入状态变化，否则应该置为不可用
        if self.table_widget.rowCount():
            disabled = checked == Qt.CheckState.Unchecked
            self.del_button.setDisabled(disabled)
        else:
            self.del_button.setDisabled(True)

    def post_process(self):
        self.search()
        # 删除按钮默认不可用
        self.del_button.setDisabled(True)
