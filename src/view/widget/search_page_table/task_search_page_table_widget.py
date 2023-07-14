# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QComboBox, QLineEdit, QLabel, QGridLayout, QWidget, QPushButton

from src.constant.window_constant import TASK_BOX_TITLE, PROJECT_NAME_LABEL_TEXT, PROJECT_NAME_PLACEHOLDER_TEXT, \
    TASK_NAME_LABEL_TEXT, TASK_NAME_PLACEHOLDER_TEXT, TASK_TYPE_LABEL_TEXT, TASK_TYPE_PLACEHOLDER_TEXT, \
    DEMAND_PERSON_LABEL_TEXT, DEMAND_PERSON_PLACEHOLDER_TEXT, PRIORITY_LABEL_TEXT, PRIORITY_PLACEHOLDER_TEXT, \
    TASK_STATUS_LABEL_TEXT, TASK_STATUS_PLACEHOLDER_TEXT, PUBLISH_STATUS_LABEL_TEXT, PUBLISH_STATUS_PLACEHOLDER_TEXT, \
    START_TIME_LABEL_TEXT, START_TIME_PLACEHOLDER_TEXT, END_TIME_LABEL_TEXT, END_TIME_PLACEHOLDER_TEXT, \
    SWITCH_ADVANCED_SEARCH_BTN_TEXT, SWITCH_BASIC_SEARCH_BTN_TEXT
from src.service.async_func.async_work_task import ListTaskExecutor
from src.view.table.table_widget.work_task_manager_table_widget import WorkTaskManagerTableWidget
from src.view.widget.search_page_table.search_page_table_widget import SearchPageTableWidget
from src.view.widget.search_page_table.search_widget_func import setup_form_combox, setup_form_lineedit

_author_ = 'luwt'
_date_ = '2023/7/12 10:49'


class TaskSearchPageTableWidget(SearchPageTableWidget):

    def __init__(self, main_window):
        self.main_window = main_window
        self.basic_search_widget: QWidget = ...
        self.basic_search_layout: QGridLayout = ...
        self.advanced_search_widget: QWidget = ...
        self.advanced_search_layout: QGridLayout = ...
        # 项目名称搜索下拉框
        self.project_name_label: QLabel = ...
        self.project_name_combobox: QComboBox = ...
        # 任务名称搜索输入框
        self.task_name_label: QLabel = ...
        self.task_name_lineedit: QLineEdit = ...
        # 任务类型搜索下拉框
        self.task_type_label: QLabel = ...
        self.task_type_combobox: QComboBox = ...
        # 任务需求方搜索下拉框
        self.demand_person_label: QLabel = ...
        self.demand_person_combobox: QComboBox = ...
        # 优先级搜索下拉框
        self.priority_label: QLabel = ...
        self.priority_combobox: QComboBox = ...
        # 任务状态搜索下拉框
        self.task_status_label: QLabel = ...
        self.task_status_combobox: QComboBox = ...
        # 发版状态搜索下拉框
        self.publish_status_label: QLabel = ...
        self.publish_status_combobox: QComboBox = ...
        # 开始时间搜索框，日历
        self.start_time_label: QLabel = ...
        self.start_time_lineedit: QLineEdit = ...
        # 结束时间搜索框，日历
        self.end_time_label: QLabel = ...
        self.end_time_lineedit: QLineEdit = ...
        # 高级查询、基本查询切换按钮
        self.switch_search_button: QPushButton = ...
        # 主数据表格
        self.table_widget: WorkTaskManagerTableWidget = ...
        super().__init__()

    def setup_search_ui(self):
        # 第一行基本查询  项目名称 优先级 任务名称
        self.basic_search_widget, self.basic_search_layout = self.setup_search_widget_layout()
        self.basic_search_layout.setColumnStretch(0, 1)
        self.basic_search_layout.setColumnStretch(1, 1)
        self.basic_search_layout.setColumnStretch(2, 2)

        self.project_name_label, self.project_name_combobox = setup_form_combox(self.basic_search_layout, 0)
        self.priority_label, self.priority_combobox = setup_form_combox(self.basic_search_layout, 1)
        self.task_name_label, self.task_name_lineedit = setup_form_lineedit(self.basic_search_layout, 2)

        # 第二行高级查询 任务类型  任务需求方  任务状态
        self.advanced_search_widget, self.advanced_search_layout = self.setup_search_widget_layout()
        self.advanced_search_layout.setColumnStretch(0, 1)
        self.advanced_search_layout.setColumnStretch(1, 1)
        self.advanced_search_layout.setColumnStretch(2, 1)

        self.task_type_label, self.task_type_combobox = setup_form_combox(self.advanced_search_layout, 0)
        self.demand_person_label, self.demand_person_combobox = setup_form_combox(self.advanced_search_layout, 1)
        self.task_status_label, self.task_status_combobox = setup_form_combox(self.advanced_search_layout, 2)

        # 第三行高级查询 发版状态 开始时间 结束时间
        self.publish_status_label, self.publish_status_combobox = setup_form_combox(self.advanced_search_layout, 0, 1)
        self.start_time_label, self.start_time_lineedit = setup_form_lineedit(self.advanced_search_layout, 1, 1)
        self.end_time_label, self.end_time_lineedit = setup_form_lineedit(self.advanced_search_layout, 2, 1)

    def setup_search_widget_layout(self):
        search_widget = QWidget()
        self._layout.addWidget(search_widget)
        search_layout = QGridLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_widget.setLayout(search_layout)
        return search_widget, search_layout

    def setup_button_ui(self, blank_left=8):
        super().setup_button_ui()
        self.switch_search_button = QPushButton()
        self.switch_search_button.setObjectName('switch_search_button')
        self.button_layout.addWidget(self.switch_search_button, 0, blank_left, 1, 1)

    def get_table_widget(self) -> WorkTaskManagerTableWidget:
        return WorkTaskManagerTableWidget(self)

    def setup_search_label_text(self):
        # 基本查询部分
        self.project_name_label.setText(PROJECT_NAME_LABEL_TEXT)
        self.priority_label.setText(PRIORITY_LABEL_TEXT)
        self.task_name_label.setText(TASK_NAME_LABEL_TEXT)
        self.project_name_combobox.setPlaceholderText(PROJECT_NAME_PLACEHOLDER_TEXT)
        self.priority_combobox.setPlaceholderText(PRIORITY_PLACEHOLDER_TEXT)
        self.task_name_lineedit.setPlaceholderText(TASK_NAME_PLACEHOLDER_TEXT)

        # 切换按钮
        self.switch_search_button.setText(SWITCH_ADVANCED_SEARCH_BTN_TEXT)

        self.setup_advanced_search_label_text()

    def setup_advanced_search_label_text(self):
        # 高级查询部分
        self.task_type_label.setText(TASK_TYPE_LABEL_TEXT)
        self.demand_person_label.setText(DEMAND_PERSON_LABEL_TEXT)
        self.task_status_label.setText(TASK_STATUS_LABEL_TEXT)
        self.publish_status_label.setText(PUBLISH_STATUS_LABEL_TEXT)
        self.start_time_label.setText(START_TIME_LABEL_TEXT)
        self.end_time_label.setText(END_TIME_LABEL_TEXT)
        self.task_type_combobox.setPlaceholderText(TASK_TYPE_PLACEHOLDER_TEXT)
        self.demand_person_combobox.setPlaceholderText(DEMAND_PERSON_PLACEHOLDER_TEXT)
        self.task_status_combobox.setPlaceholderText(TASK_STATUS_PLACEHOLDER_TEXT)
        self.publish_status_combobox.setPlaceholderText(PUBLISH_STATUS_PLACEHOLDER_TEXT)
        self.start_time_lineedit.setPlaceholderText(START_TIME_PLACEHOLDER_TEXT)
        self.end_time_lineedit.setPlaceholderText(END_TIME_PLACEHOLDER_TEXT)

    def connect_signal(self):
        self.switch_search_button.clicked.connect(self.switch_search_mode)
        super().connect_signal()

    def switch_search_mode(self):
        # 高级查询模式
        if self.advanced_search_widget.isVisible():
            # 关闭高级查询模式时，清空高级查询输入的数据
            self.reset_advanced_search_data()
            self.advanced_search_widget.setVisible(False)
            self.switch_search_button.setText(SWITCH_ADVANCED_SEARCH_BTN_TEXT)
        else:
            self.advanced_search_widget.setVisible(True)
            self.switch_search_button.setText(SWITCH_BASIC_SEARCH_BTN_TEXT)

    def reset_search_data(self):
        self.reset_basic_search_data()
        self.reset_advanced_search_data()

    def reset_basic_search_data(self):
        self.project_name_combobox.setCurrentIndex(-1)
        self.priority_combobox.setCurrentIndex(-1)
        self.task_name_lineedit.clear()

    def reset_advanced_search_data(self):
        self.task_type_combobox.setCurrentIndex(-1)
        self.demand_person_combobox.setCurrentIndex(-1)
        self.task_status_combobox.setCurrentIndex(-1)
        self.publish_status_combobox.setCurrentIndex(-1)
        self.start_time_lineedit.clear()
        self.end_time_lineedit.clear()

    def get_search_executor(self):
        return ListTaskExecutor(self.main_window, self.main_window, TASK_BOX_TITLE, self.table_widget.fill_table)

    def del_rows(self):
        ...

    def post_process(self):
        super().post_process()
        # 默认隐藏高级查询
        self.advanced_search_widget.setVisible(False)
