# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.constant.help_constant import TASK_DETAIL_HELP
from src.constant.task_constant import TASK_NAME_LABEL_TEXT, BASIC_INFO_TEXT, FEATURE_INFO_TEXT, ATTACHMENT_INFO_TEXT, \
    PUBLISH_INFO_TEXT, COMMENT_INFO_TEXT, TASK_DETAIL_BOX_TITLE, EDIT_TASK_BOX_TITLE, ADD_TASK_BOX_TITLE
from src.service.async_func.async_work_task import TaskDetailExecutor, AddTaskExecutor, EditTaskExecutor
from src.service.system_storage.task_sqlite import Task
from src.service.util.task_cache_util import get_task_names
from src.view.frame.stacked_dialog_frame import StackedDialogFrame
from src.view.widget.task_detail.task_basic_info_widget import TaskBasicInfoWidget
from src.view.widget.task_detail.task_feature_info_widget import TaskFeatureInfoWidget

_author_ = 'luwt'
_date_ = '2023/7/26 9:10'


class TaskDetailDialogFrame(StackedDialogFrame):
    """任务详情对话框框架"""
    save_signal = pyqtSignal(Task)
    edit_signal = pyqtSignal(Task)

    def __init__(self, parent_dialog, dialog_title, task_id=None):
        self.dialog_data: Task = ...
        self.new_dialog_data: Task = ...

        # 第一个窗口，基本信息
        self.basic_info_widget: TaskBasicInfoWidget = ...
        # 第二个窗口，特征信息
        self.feature_info_widget: TaskFeatureInfoWidget = ...
        # 第三个窗口，附件信息

        # 第四个窗口，发版信息

        # 第五个窗口，评论信息

        self.add_task_executor: AddTaskExecutor = ...
        self.edit_task_executor: EditTaskExecutor = ...
        super().__init__(parent_dialog, dialog_title, get_task_names(), task_id)

    def get_new_dialog_data(self) -> Task:
        return Task()

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def fill_list_widget(self):
        self.list_widget.addItem(BASIC_INFO_TEXT)
        self.list_widget.addItem(FEATURE_INFO_TEXT)
        self.list_widget.addItem(ATTACHMENT_INFO_TEXT)
        self.list_widget.addItem(PUBLISH_INFO_TEXT)
        self.list_widget.addItem(COMMENT_INFO_TEXT)

    def fill_stacked_widget(self):
        # 第一个窗口，基本信息
        self.basic_info_widget = TaskBasicInfoWidget()
        # 构建名称输入表单
        self.setup_name_form()
        self.basic_info_widget.setup_ui(self.name_layout)
        self.stacked_widget.addWidget(self.basic_info_widget)

        # 第二个窗口，特征信息
        self.feature_info_widget = TaskFeatureInfoWidget()
        self.feature_info_widget.setup_ui()
        self.stacked_widget.addWidget(self.feature_info_widget)

    def setup_other_label_text(self):
        self.name_label.setText(TASK_NAME_LABEL_TEXT)
        self.basic_info_widget.setup_label_text()
        self.feature_info_widget.setup_label_text()

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        return TASK_DETAIL_HELP

    def collect_input(self):
        self.new_dialog_data.task_name = self.name_input.text()
        self.basic_info_widget.collect_data(self.new_dialog_data)
        self.feature_info_widget.collect_data(self.new_dialog_data)

    def button_available(self) -> bool:
        # 名称可用，并且特征信息都存在
        return self.name_input.displayText() and self.name_available and self.feature_info_widget.check_data()

    def check_data_changed(self) -> bool:
        return self.dialog_data != self.new_dialog_data

    def connect_child_signal(self):
        self.feature_info_widget.data_changed_signal.connect(self.check_input)

    def save_func(self):
        self.collect_input()
        # 编辑
        if self.dialog_data:
            self.new_dialog_data.id = self.dialog_data.id
            self.edit_task_executor = EditTaskExecutor(self.new_dialog_data, self.parent_dialog,
                                                       self.parent_dialog, EDIT_TASK_BOX_TITLE, self.edit_callback)
            self.edit_task_executor.start()
        else:
            self.add_task_executor = AddTaskExecutor(self.new_dialog_data, self.parent_dialog,
                                                     self.parent_dialog, ADD_TASK_BOX_TITLE, self.add_callback)
            self.add_task_executor.start()

    def edit_callback(self):
        self.edit_signal.emit(self.new_dialog_data)
        self.parent_dialog.close()

    def add_callback(self):
        self.save_signal.emit(self.new_dialog_data)
        self.parent_dialog.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def get_read_storage_executor(self, callback):
        return TaskDetailExecutor(self.dialog_data, self.parent_dialog, self.parent_dialog,
                                  TASK_DETAIL_BOX_TITLE, callback)

    def get_old_name(self) -> str:
        return self.dialog_data.task_name

    def setup_echo_other_data(self):
        self.basic_info_widget.echo_data(self.dialog_data)
        self.feature_info_widget.echo_data(self.dialog_data)

    # ------------------------------ 后置处理 end ------------------------------ #
