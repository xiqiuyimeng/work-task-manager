# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QPushButton, QLabel

from src.constant.help_constant import PROJECT_TABLE_HELP
from src.constant.project_constant import ADD_PROJECT_BUTTON_TEXT, DEL_PROJECT_BUTTON_TEXT, EDIT_PROJECT_TITLE, \
    ADD_PROJECT_TITLE, DEL_PROJECT_PROMPT, DEL_PROJECT_TITLE, BATCH_DEL_PROJECT_PROMPT
from src.service.async_func.async_project_task import DelProjectExecutor, BatchDelProjectExecutor
from src.service.util.project_cache_util import get_project_dict_list, get_project
from src.view.box.message_box import pop_question
from src.view.dialog.project.project_detail_dialog import ProjectDetailDialog
from src.view.frame.dialog_frame_abc import DialogFrameABC
from src.view.table.table_widget.project_table_widget import ProjectTableWidget
from src.view.window.main_window_func import get_window

_author_ = 'luwt'
_date_ = '2023/7/18 11:25'


class ProjectDialogFrame(DialogFrameABC):
    """项目列表对话框框架"""

    def __init__(self, *args, **kwargs):
        # 操作表格按钮布局
        self.operation_table_btn_layout: QGridLayout = ...
        # 添加新行按钮
        self.add_row_button: QPushButton = ...
        # 删除行按钮
        self.del_row_button: QPushButton = ...
        # 主体表格
        self.table_widget: ProjectTableWidget = ...
        # 删除行数据执行器
        self.del_project_executor: DelProjectExecutor = ...
        # 批量删除执行器
        self.batch_del_project_executor: BatchDelProjectExecutor = ...
        # 项目详情对话框
        self.project_detail_dialog: ProjectDetailDialog = ...
        super().__init__(*args, **kwargs)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        # 操作按钮组
        self.operation_table_btn_layout = QGridLayout()
        self.setup_operation_button()
        self.frame_layout.addLayout(self.operation_table_btn_layout)
        # 创建表格
        self.table_widget = ProjectTableWidget(self)
        self.frame_layout.addWidget(self.table_widget)

    def setup_operation_button(self):
        self.operation_table_btn_layout.addWidget(QLabel(), 0, 0, 1, 4)
        self.add_row_button = QPushButton()
        self.add_row_button.setObjectName('create_row_button')
        self.operation_table_btn_layout.addWidget(self.add_row_button, 0, 4, 1, 1)
        self.del_row_button = QPushButton()
        self.del_row_button.setObjectName('del_row_button')
        self.operation_table_btn_layout.addWidget(self.del_row_button, 0, 5, 1, 1)

    def setup_other_label_text(self):
        self.add_row_button.setText(ADD_PROJECT_BUTTON_TEXT)
        self.del_row_button.setText(DEL_PROJECT_BUTTON_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        return PROJECT_TABLE_HELP

    def connect_other_signal(self):
        # 添加行按钮点击，打开添加行对话框
        self.add_row_button.clicked.connect(lambda: self.open_row_data_dialog())
        # # 连接表格中行编辑信号
        self.table_widget.row_edit_signal.connect(self.open_row_data_dialog)
        # # 连接表格中行删除信号
        self.table_widget.row_del_signal.connect(self.del_row)
        # 连接表头复选框状态变化信号
        self.table_widget.header_widget.header_check_changed.connect(self.set_del_btn_available)
        # 删除行按钮点击信号
        self.del_row_button.clicked.connect(self.del_rows)

    def open_row_data_dialog(self, row_id=None, row_index=None):
        exists_project_names = [self.table_widget.item(row, 1).text()
                                for row in range(self.table_widget.rowCount())]
        if row_id:
            project = get_project(row_id)
            self.project_detail_dialog = ProjectDetailDialog(EDIT_PROJECT_TITLE, exists_project_names, project)
            self.project_detail_dialog.edit_signal.connect(lambda data: self.table_widget.edit_row(row_index, data))
        else:
            self.project_detail_dialog = ProjectDetailDialog(ADD_PROJECT_TITLE, exists_project_names)
            self.project_detail_dialog.save_signal.connect(self.table_widget.add_row)
        self.project_detail_dialog.exec()

    def del_row(self, row_id, row_index, item_name):
        if not pop_question(DEL_PROJECT_PROMPT.format(item_name), DEL_PROJECT_TITLE, self):
            return
        self.del_project_executor = DelProjectExecutor(row_id, item_name, row_index, self.parent_dialog,
                                                       self.parent_dialog, DEL_PROJECT_TITLE,
                                                       self.del_callback)
        self.del_project_executor.start()

    def del_callback(self, row_index):
        self.table_widget.del_row(row_index)
        # 更新主界面搜索下拉框，删除数据
        get_window().task_table_widget.del_project_combobox_item((row_index,))

    def set_del_btn_available(self, checked):
        # 当表格存在行，再动态渲染删除按钮状态，否则置为不可用
        if self.table_widget.rowCount():
            self.del_row_button.setDisabled(checked == Qt.CheckState.Unchecked)
        else:
            self.del_row_button.setDisabled(True)

    def del_rows(self):
        # 收集所有选中项数据，进行删除
        delete_ids, delete_names, delete_index_list = self.table_widget.get_checked_id_name_index_list()
        if not pop_question(BATCH_DEL_PROJECT_PROMPT.format(len(delete_ids)), DEL_PROJECT_TITLE, self):
            return
        self.batch_del_project_executor = BatchDelProjectExecutor(delete_ids, delete_names, delete_index_list,
                                                                  self.parent_dialog, self.parent_dialog,
                                                                  DEL_PROJECT_TITLE, self.batch_del_callback)
        self.batch_del_project_executor.start()

    def batch_del_callback(self, row_index_list):
        # 更新主界面搜索下拉框，删除数据
        get_window().task_table_widget.del_project_combobox_item(reversed(row_index_list))
        self.table_widget.del_rows()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        # 获取项目列表数据，填充表格
        project_list = get_project_dict_list()
        if project_list:
            self.table_widget.fill_table(project_list)
        # 初始化按钮状态
        self.set_del_btn_available(Qt.CheckState.Unchecked)

    # ------------------------------ 后置处理 end ------------------------------ #
