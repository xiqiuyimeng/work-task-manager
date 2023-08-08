# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QGridLayout, QPushButton

from src.constant.data_dict_dialog_constant import SYNC_DEFAULT_DATA_DICT_BTN_TEXT, DEL_DATA_DICT_BTN_TEXT, \
    ADD_DATA_DICT_BTN_TEXT, DATA_DICT_DETAIL_TIP, DATA_DICT_DETAIL_BOX_TITLE, BLANK_DATA_DICT_NAME_PROMPT, \
    QUERY_DATA_DICT_BIND_DATA_TITLE, NO_DATA_DICT_PROMPT
from src.constant.help_constant import DATA_DICT_DETAIL_HELP
from src.enum.data_dict_enum import DataDictTypeEnum
from src.service.async_func.async_data_dict_task import SaveDataDictExecutor, QueryDataDictBindDataExecutor
from src.service.util.data_dict_cache_util import get_data_dict_list, get_data_dict
from src.view.box.message_box import pop_fail
from src.view.dialog.data_dict.data_dict_bind_dialog import DataDictBindDialog
from src.view.frame.save_dialog_frame import SaveDialogFrame
from src.view.table.table_widget.data_dict_table_widget import DataDictTableWidget
from src.view.window.main_window_func import get_window

_author_ = 'luwt'
_date_ = '2023/7/15 12:05'


class DataDictDetailDialogFrame(SaveDialogFrame):
    """数据字典详情对话框框架"""

    def __init__(self, data_dict_type, *args):
        # 加载当前类型的数据
        self.data_dict_type = data_dict_type
        self.data_dict_type_code = self.data_dict_type[0]
        self.data_dict_list = get_data_dict_list(self.data_dict_type_code)
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
        # 处理需要重新绑定数据的数据字典项对话框
        self.data_dict_bind_dialog: DataDictBindDialog = ...
        # 保存数据执行器
        self.save_data_executor: SaveDataDictExecutor = ...
        # 读取数据字典关联数据执行器
        self.query_bind_data_executor: QueryDataDictBindDataExecutor = ...
        self.bind_data_dict_ids: list = ...
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
        return DATA_DICT_DETAIL_HELP

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
        self.table_widget.add_new_data_dict(self.data_dict_type_code)

    def set_del_btn_available(self, checked):
        # 当表格存在行，再动态渲染删除按钮状态，否则置为不可用
        if self.table_widget.rowCount():
            self.del_button.setDisabled(checked == Qt.CheckState.Unchecked)
        else:
            self.del_button.setDisabled(True)

    def save_func(self):
        data_dict_list = self.table_widget.collect_data()
        # 名称检查
        for data_dict in data_dict_list:
            if not data_dict.dict_name:
                pop_fail(BLANK_DATA_DICT_NAME_PROMPT, DATA_DICT_DETAIL_BOX_TITLE, self.parent_dialog)
                return

        # 检查绑定数据是否需要重新分配
        if self.bind_data_dict_ids is not Ellipsis and self.bind_data_dict_ids:
            # 如果存在需要分配的字典项，但是新的字典项为空，提示报错
            if not data_dict_list:
                pop_fail(NO_DATA_DICT_PROMPT, DATA_DICT_DETAIL_BOX_TITLE, self.parent_dialog)
                return
            self.handle_bind_data_dict(data_dict_list)
        else:
            self.do_save_data(data_dict_list)

    def do_save_data(self, data_dict_list):
        self.save_data_executor = SaveDataDictExecutor(self.data_dict_type_code, data_dict_list,
                                                       self.parent_dialog, self.parent_dialog,
                                                       DATA_DICT_DETAIL_BOX_TITLE, self.save_callback)
        self.save_data_executor.start()

    def handle_bind_data_dict(self, data_dict_list):
        save_data_dict_ids = {data_dict.id for data_dict in data_dict_list}
        bind_data_dict_list = list()
        for bind_data_dict_id in self.bind_data_dict_ids:
            # 获取已删除且绑定数据的原字典项
            bind_data_dict = get_data_dict(self.data_dict_type_code, bind_data_dict_id)
            # 如果字典项已删除（不在需要保存的数据中），并且原字典项也不在新数据中
            if bind_data_dict_id not in save_data_dict_ids:
                bind_data_dict_list.append(bind_data_dict)
        # 如果存在需要重新分配的数据，打开处理对话框
        if bind_data_dict_list:
            self.data_dict_bind_dialog = DataDictBindDialog(bind_data_dict_list, data_dict_list)
            self.data_dict_bind_dialog.save_signal.connect(lambda: self.do_save_data(data_dict_list))
            self.data_dict_bind_dialog.exec()
        else:
            self.do_save_data(data_dict_list)

    def save_callback(self):
        # 更新主页面数据字典搜索下拉框值
        if self.data_dict_type_code != DataDictTypeEnum.publish_type.value[0]:
            task_table_widget = get_window().task_table_widget
            task_table_widget.update_data_dict_combobox(self.data_dict_type_code)
            # 刷新页面数据，以更新字典项值
            task_table_widget.search()
        self.parent_dialog.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        super().post_process()
        # 清除焦点
        self.sync_default_values_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.add_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.del_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.set_del_btn_available(Qt.CheckState.Unchecked)
        # 加载数据
        if self.data_dict_list:
            self.table_widget.fill_table(self.data_dict_list)
            data_dict_ids = [data_dict.id for data_dict in self.data_dict_list]
            self.query_bind_data_executor = QueryDataDictBindDataExecutor(self.data_dict_type_code, data_dict_ids,
                                                                          self.parent_dialog, self.parent_dialog,
                                                                          QUERY_DATA_DICT_BIND_DATA_TITLE,
                                                                          self.query_bind_data_callback)
            self.query_bind_data_executor.start()

    def query_bind_data_callback(self, data_dict_ids):
        self.bind_data_dict_ids = data_dict_ids

    # ------------------------------ 后置处理 end ------------------------------ #
