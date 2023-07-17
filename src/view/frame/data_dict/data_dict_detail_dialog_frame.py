# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QGridLayout, QPushButton

from src.constant.data_dict_dialog_constant import SYNC_DEFAULT_DATA_DICT_BTN_TEXT, \
    DEL_DATA_DICT_BTN_TEXT, ADD_DATA_DICT_BTN_TEXT, DATA_DICT_DETAIL_TIP, DATA_DICT_DETAIL_BOX_TITLE, \
    BLANK_DATA_DICT_NAME_PROMPT
from src.service.async_func.async_data_dict_task import SaveDataDictExecutor
from src.service.util.data_dict_cache_util import get_data_dict
from src.view.box.message_box import pop_fail
from src.view.frame.save_dialog_frame import SaveDialogFrame
from src.view.table.table_widget.data_dict_table_widget import DataDictTableWidget
from src.view.widget.search_page_table.search_widget_func import update_data_dict_combobox
from src.view.window.main_window_func import get_window

_author_ = 'luwt'
_date_ = '2023/7/15 12:05'


class DataDictDetailDialogFrame(SaveDialogFrame):
    """数据字典详情对话框框架"""

    def __init__(self, data_dict_type, *args):
        # 加载当前类型的数据
        self.data_dict_type = data_dict_type
        self.data_dict_list = get_data_dict(self.data_dict_type[0])
        # 表格顶部布局
        self.table_button_layout: QGridLayout = ...
        # 温馨提示
        self.tip_label: QLabel = ...
        # 同步默认值列表
        self.sync_default_values_button: QPushButton = ...
        # 添加按钮
        self.add_button: QPushButton = ...
        # 删除按钮
        self.del_button: QPushButton = ...
        # 主体数据表格
        self.table_widget: DataDictTableWidget = ...
        # 保存数据执行器
        self.save_data_executor: SaveDataDictExecutor = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        self.tip_label = QLabel()
        self.tip_label.setObjectName('tips_label')
        self.frame_layout.addWidget(self.tip_label)
        self.table_button_layout = QGridLayout()
        self.frame_layout.addLayout(self.table_button_layout)
        self.table_button_layout.addWidget(QLabel(), 0, 0, 1, 3)
        self.sync_default_values_button = QPushButton()
        self.sync_default_values_button.setObjectName('sync_default_values_button')
        self.table_button_layout.addWidget(self.sync_default_values_button, 0, 3, 1, 2)
        self.add_button = QPushButton()
        self.add_button.setObjectName('create_row_button')
        self.table_button_layout.addWidget(self.add_button, 0, 5, 1, 1)
        self.del_button = QPushButton()
        self.del_button.setObjectName('del_button')
        self.table_button_layout.addWidget(self.del_button, 0, 6, 1, 1)

        self.table_widget = DataDictTableWidget(self)
        self.frame_layout.addWidget(self.table_widget)

    def setup_other_label_text(self):
        self.tip_label.setText(DATA_DICT_DETAIL_TIP)
        self.sync_default_values_button.setText(SYNC_DEFAULT_DATA_DICT_BTN_TEXT)
        self.add_button.setText(ADD_DATA_DICT_BTN_TEXT)
        self.del_button.setText(DEL_DATA_DICT_BTN_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        ...

    def connect_other_signal(self):
        # 同步默认的数据字典
        self.sync_default_values_button.clicked.connect(self.sync_default_data_dict)
        self.add_button.clicked.connect(self.add_new_data_dict)
        self.del_button.clicked.connect(self.table_widget.del_rows)
        self.table_widget.header_widget.header_check_changed.connect(self.set_del_btn_available)

    def sync_default_data_dict(self):
        # 同步默认数据字典列表
        self.table_widget.sync_default_data_dict(self.data_dict_type)

    def add_new_data_dict(self):
        self.table_widget.add_new_data_dict(self.data_dict_type[0])

    def set_del_btn_available(self, checked):
        # 当表格存在行，再动态渲染删除按钮状态，否则置为不可用
        if self.table_widget.rowCount():
            self.del_button.setDisabled(checked == Qt.CheckState.Unchecked)
        else:
            self.del_button.setDisabled(True)

    def save_func(self):
        data_dict_list = self.table_widget.collect_data()
        for data_dict in data_dict_list:
            if not data_dict.dict_name:
                pop_fail(BLANK_DATA_DICT_NAME_PROMPT, DATA_DICT_DETAIL_BOX_TITLE, self.parent_dialog)
                return
        self.save_data_executor = SaveDataDictExecutor(data_dict_list, self.parent_dialog, self.parent_dialog,
                                                       DATA_DICT_DETAIL_BOX_TITLE, self.save_callback)
        self.save_data_executor.start()

    def save_callback(self):
        # 获取主页面搜索下拉框和数据字典类型映射字典
        combobox_dict = get_window().task_table_widget.data_dict_type_combobox_dict
        update_data_dict_combobox(combobox_dict.get(self.data_dict_type[0]), self.data_dict_type[0])
        self.parent_dialog.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        self.set_del_btn_available(Qt.CheckState.Unchecked)
        # 加载数据
        if self.data_dict_list:
            self.table_widget.fill_table(self.data_dict_list)

    # ------------------------------ 后置处理 end ------------------------------ #
