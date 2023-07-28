# -*- coding: utf-8 -*-

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel

from src.constant.task_constant import EDIT_TASK_TITLE, ADD_TASK_TITLE
from src.constant.window_constant import RESET_SEARCH_BTN_TEXT, SEARCH_BTN_TEXT, DEL_BTN_TEXT, ADD_BTN_TEXT
from src.service.async_func.async_task_abc import LoadingMaskThreadExecutor
from src.view.box.message_box import pop_question
from src.view.custom_widget.page.page_widget import PageWidget
from src.view.dialog.custom_dialog_abc import CustomSaveDialogABC
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
        # 重置、查询、添加、删除按钮
        self.reset_search_button: QPushButton = ...
        self.search_button: QPushButton = ...
        self.add_button: QPushButton = ...
        self.del_button: QPushButton = ...
        # 数据表格
        self.table_widget: CustomTableWidget = ...
        # 分页组件
        self.page_widget: PageWidget = ...
        # 搜索数据列表执行器
        self.search_executor: LoadingMaskThreadExecutor = ...
        # 行具体信息对话框
        self.row_data_dialog: CustomSaveDialogABC = ...
        # 删除行数据执行器
        self.del_data_executor: LoadingMaskThreadExecutor = ...
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

    def setup_button_ui(self, blank_left=6):
        self.add_button = QPushButton()
        self.add_button.setObjectName('add_button')
        self.button_layout.addWidget(self.add_button, 0, 0, 1, 1)
        self.del_button = QPushButton()
        self.del_button.setObjectName('del_button')
        self.button_layout.addWidget(self.del_button, 0, 1, 1, 1)
        self.button_layout.addWidget(QLabel(), 0, 2, 1, blank_left)
        self.reset_search_button = QPushButton()
        self.reset_search_button.setObjectName('reset_button')
        self.button_layout.addWidget(self.reset_search_button, 0, blank_left + 2, 1, 1)
        # 留一个空位
        self.search_button = QPushButton()
        self.search_button.setObjectName('search_button')
        self.button_layout.addWidget(self.search_button, 0, blank_left + 4, 1, 1)

    def get_table_widget(self) -> CustomTableWidget:
        ...

    def setup_label_text(self):
        self.reset_search_button.setText(RESET_SEARCH_BTN_TEXT)
        self.search_button.setText(SEARCH_BTN_TEXT)
        self.del_button.setText(DEL_BTN_TEXT)
        self.add_button.setText(ADD_BTN_TEXT)
        self.setup_search_label_text()

    def setup_search_label_text(self):
        ...

    def connect_signal(self):
        self.reset_search_button.clicked.connect(self.reset_search)
        self.search_button.clicked.connect(self.search)
        self.add_button.clicked.connect(lambda: self.open_row_data_dialog())
        self.del_button.clicked.connect(self.del_rows)
        # 表格表头选中状态变化
        self.table_widget.header_widget.header_check_changed.connect(self.set_button_available)
        # 表格选中行编辑信号
        self.table_widget.row_edit_signal.connect(self.open_row_data_dialog)
        # 表格选中行删除信号
        self.table_widget.row_del_signal.connect(lambda row_id, index, item_name: self.del_row(row_id, item_name))

    def reset_search(self):
        # 清空数据
        self.reset_search_data()
        # 重新搜索
        self.search()

    def reset_search_data(self):
        ...

    def search(self):
        self.search_executor = self.get_search_executor(self.search_callback)
        # 添加搜索条件
        self.search_executor.start()

    def get_search_executor(self, search_callback) -> LoadingMaskThreadExecutor:
        ...

    def search_callback(self, data_list):
        # 首先清除页面数据
        if self.table_widget.rowCount():
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
        # 重新填充数据
        self.table_widget.fill_table(data_list)

    def open_row_data_dialog(self, row_id=None, row_index=None):
        if row_id:
            self.row_data_dialog = self.get_row_data_dialog(EDIT_TASK_TITLE, row_id)
            self.row_data_dialog.edit_signal.connect(lambda data: self.table_widget.edit_row(row_index, data))
        else:
            self.row_data_dialog = self.get_row_data_dialog(ADD_TASK_TITLE, row_id)
            self.row_data_dialog.save_signal.connect(self.search)
        self.row_data_dialog.exec()

    def get_row_data_dialog(self, title, row_id) -> CustomSaveDialogABC:
        ...

    def del_rows(self):
        # 收集所有选中项数据，进行删除
        delete_ids, delete_names, del_indexes = self.table_widget.get_checked_id_name_index_list()
        batch_del_prompt, batch_del_title = self.get_batch_del_prompt_title()
        if not pop_question(batch_del_prompt.format(len(delete_ids)), batch_del_title, self):
            return
        self.do_del_rows(delete_ids, delete_names, batch_del_title)

    def get_batch_del_prompt_title(self) -> tuple:
        ...

    def do_del_rows(self, delete_ids, delete_names, del_title):
        self.del_data_executor = self.get_del_row_executor(delete_ids, delete_names, del_title, self.search)
        self.del_data_executor.start()

    def get_del_row_executor(self, delete_ids, delete_names, del_title, del_callback) -> LoadingMaskThreadExecutor:
        ...

    def set_button_available(self, checked):
        # 如果表格存在行，删除按钮状态根据传入状态变化，否则应该置为不可用
        if self.table_widget.rowCount():
            disabled = checked == Qt.CheckState.Unchecked
            self.del_button.setDisabled(disabled)
        else:
            self.del_button.setDisabled(True)

    def del_row(self, row_id, item_name):
        del_prompt, del_title = self.get_del_prompt_title()
        if not pop_question(del_prompt.format(item_name), del_title, self):
            return
        self.do_del_rows((row_id,), (item_name,), del_title)

    def get_del_prompt_title(self) -> tuple:
        ...

    def post_process(self):
        self.search()
        # 删除按钮默认不可用
        self.del_button.setDisabled(True)
        self.page_widget.init_page_data()
