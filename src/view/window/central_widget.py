# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout

from src.constant.window_constant import TASK_BOX_TITLE
from src.service.async_func.async_work_task import ListTaskExecutor
from src.view.table.table_widget.work_task_manager_table_widget import WorkTaskManagerTableWidget

_author_ = 'luwt'
_date_ = '2023/7/10 14:04'


class CentralWidget(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._layout: QVBoxLayout = ...
        # 搜索区域
        self.search_layout: QGridLayout = ...
        # 项目名称搜索下拉框
        self.project_name_search = ...
        # 任务名称搜索输入框
        # 任务类型搜索下拉框
        # 任务需求方搜索下拉框
        # 优先级搜索下拉框
        # 任务状态搜索下拉框
        # 是否发版搜索下拉框
        # 开始时间搜索框，日历
        # 结束时间搜索框，日历
        # 主体表格内容区
        self.table_widget: WorkTaskManagerTableWidget = ...
        # 分页组件
        # 读取任务列表执行器
        self.list_task_executor: ListTaskExecutor = ...

    def setup_ui(self):
        self._layout = QVBoxLayout(self)

        # 搜索区
        self.search_layout = QGridLayout()
        self._layout.addLayout(self.search_layout)


        # 主数据区
        self.table_widget = WorkTaskManagerTableWidget(self)
        self._layout.addWidget(self.table_widget)

    def fill_data(self):
        self.list_task_executor = ListTaskExecutor(self.main_window, self.main_window,
                                                   TASK_BOX_TITLE, self.table_widget.fill_table)
        self.list_task_executor.start()
