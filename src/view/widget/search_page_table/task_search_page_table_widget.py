# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QComboBox, QLineEdit, QLabel, QGridLayout, QWidget, QPushButton

from src.constant.task_constant import BATCH_DEL_TASK_PROMPT, DEL_TASK_BOX_TITLE, DEL_TASK_PROMPT
from src.constant.task_constant import PROJECT_NAME_LABEL_TEXT, PROJECT_NAME_PLACEHOLDER_TEXT, TASK_NAME_LABEL_TEXT, \
    TASK_NAME_PLACEHOLDER_TEXT, TASK_TYPE_LABEL_TEXT, TASK_TYPE_PLACEHOLDER_TEXT, DEMAND_PERSON_LABEL_TEXT, \
    DEMAND_PERSON_PLACEHOLDER_TEXT, PRIORITY_LABEL_TEXT, PRIORITY_PLACEHOLDER_TEXT, TASK_STATUS_LABEL_TEXT, \
    TASK_STATUS_PLACEHOLDER_TEXT, PUBLISH_STATUS_LABEL_TEXT, PUBLISH_STATUS_PLACEHOLDER_TEXT, \
    START_TIME_LABEL_TEXT, START_TIME_PLACEHOLDER_TEXT, END_TIME_LABEL_TEXT, END_TIME_PLACEHOLDER_TEXT
from src.constant.window_constant import SWITCH_ADVANCED_SEARCH_BTN_TEXT, SWITCH_BASIC_SEARCH_BTN_TEXT, TASK_BOX_TITLE
from src.enum.data_dict_enum import DataDictTypeEnum
from src.service.async_func.async_work_task import ListTaskExecutor, DelTaskExecutor
from src.service.system_storage.task_sqlite import BasicTask
from src.view.custom_widget.calendar_time_lineedit import CalendarTimeLineEdit
from src.view.dialog.task.task_detail_dialog import TaskDetailDialog
from src.view.table.table_widget.task_manager_table_widget import WorkTaskManagerTableWidget
from src.view.widget.search_page_table.search_page_table_widget import SearchPageTableWidget
from src.view.widget.widget_func import setup_grid_form_combox, setup_form_lineedit, fill_project_combobox, \
    fill_data_dict_combobox, update_data_dict_combobox, add_project_combobox_item, update_project_combobox_item, \
    get_combobox_data

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
        self.start_time_lineedit: CalendarTimeLineEdit = ...
        # 结束时间搜索框，日历
        self.end_time_label: QLabel = ...
        self.end_time_lineedit: CalendarTimeLineEdit = ...
        # 高级查询、基本查询切换按钮
        self.switch_search_button: QPushButton = ...

        # 数据字典搜索下拉框与数据字典类型关系
        self.data_dict_type_combobox_dict = dict()
        super().__init__()

    def setup_search_ui(self):
        # 第一行基本查询
        self.setup_basic_search()

        # 第二行第三行高级查询
        self.setup_advanced_search()

    def setup_search_widget_layout(self):
        search_widget = QWidget()
        self._layout.addWidget(search_widget)
        search_layout = QGridLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_widget.setLayout(search_layout)
        return search_widget, search_layout

    def setup_basic_search(self):
        # 项目名称 优先级 任务名称
        self.basic_search_widget, self.basic_search_layout = self.setup_search_widget_layout()
        self.basic_search_layout.setColumnStretch(0, 3)
        self.basic_search_layout.setColumnStretch(1, 2)
        self.basic_search_layout.setColumnStretch(2, 4)

        self.project_name_label, self.project_name_combobox = setup_grid_form_combox(self.basic_search_layout, 0)
        self.priority_label, self.priority_combobox = setup_grid_form_combox(self.basic_search_layout, 1)
        self.task_name_label, self.task_name_lineedit = setup_form_lineedit(self.basic_search_layout, 2)

    def setup_advanced_search(self):
        # 第二行高级查询 任务类型  任务需求方  任务状态
        self.advanced_search_widget, self.advanced_search_layout = self.setup_search_widget_layout()
        self.advanced_search_layout.setColumnStretch(0, 1)
        self.advanced_search_layout.setColumnStretch(1, 1)
        self.advanced_search_layout.setColumnStretch(2, 1)

        self.task_type_label, self.task_type_combobox = setup_grid_form_combox(self.advanced_search_layout, 0)
        self.demand_person_label, self.demand_person_combobox = setup_grid_form_combox(self.advanced_search_layout, 1)
        self.task_status_label, self.task_status_combobox = setup_grid_form_combox(self.advanced_search_layout, 2)

        # 第三行高级查询 发版状态 开始时间 结束时间
        self.publish_status_label, self.publish_status_combobox = setup_grid_form_combox(self.advanced_search_layout,
                                                                                         0, 1)
        self.start_time_label, self.start_time_lineedit = setup_form_lineedit(self.advanced_search_layout, 1, 1,
                                                                              lineedit_class=CalendarTimeLineEdit)
        self.end_time_label, self.end_time_lineedit = setup_form_lineedit(self.advanced_search_layout, 2, 1,
                                                                          lineedit_class=CalendarTimeLineEdit)

    def setup_button_ui(self, blank_left=6):
        super().setup_button_ui()
        self.switch_search_button = QPushButton()
        self.switch_search_button.setObjectName('switch_search_button')
        self.button_layout.addWidget(self.switch_search_button, 0, blank_left + 3, 1, 1)

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
            # 清空数据后，触发查询
            self.search()
            # 关闭高级查询，隐藏高级搜索模块，并将按钮文本切换
            self.advanced_search_widget.setVisible(False)
            self.switch_search_button.setText(SWITCH_ADVANCED_SEARCH_BTN_TEXT)
        else:
            # 展示高级查询模块，切换按钮文本
            self.advanced_search_widget.setVisible(True)
            self.switch_search_button.setText(SWITCH_BASIC_SEARCH_BTN_TEXT)

    def reset_search_data(self):
        """重置搜索参数值"""
        self.reset_basic_search_data()
        self.reset_advanced_search_data()

    def reset_basic_search_data(self):
        self.reset_project_name_combobox()
        self.priority_combobox.setCurrentIndex(-1)
        self.task_name_lineedit.clear()

    def reset_project_name_combobox(self):
        self.project_name_combobox.setCurrentIndex(-1)

    def reset_advanced_search_data(self):
        """重置高级搜索参数值"""
        self.task_type_combobox.setCurrentIndex(-1)
        self.demand_person_combobox.setCurrentIndex(-1)
        self.task_status_combobox.setCurrentIndex(-1)
        self.publish_status_combobox.setCurrentIndex(-1)
        self.start_time_lineedit.clear()
        self.end_time_lineedit.clear()

    def collect_search_param(self):
        search_param = BasicTask()
        search_param.task_name = self.task_name_lineedit.text()
        get_combobox_data(self.project_name_combobox, search_param, 'project_id')
        get_combobox_data(self.priority_combobox, search_param, 'priority_id')
        get_combobox_data(self.task_type_combobox, search_param, 'task_type_id')
        get_combobox_data(self.demand_person_combobox, search_param, 'demand_person_id')
        get_combobox_data(self.task_status_combobox, search_param, 'status_id')
        get_combobox_data(self.publish_status_combobox, search_param, 'publish_status_id')
        search_param.start_time = self.start_time_lineedit.text()
        search_param.end_time = self.end_time_lineedit.text()
        return search_param

    def get_search_executor(self, search_callback):
        search_param = self.collect_search_param()
        page = self.page_widget.page_data
        return ListTaskExecutor(search_param, page, self.main_window, self.main_window,
                                TASK_BOX_TITLE, search_callback)

    def get_row_data_dialog(self, title, row_id) -> TaskDetailDialog:
        return TaskDetailDialog(title, row_id)

    def get_batch_del_prompt_title(self) -> tuple:
        return BATCH_DEL_TASK_PROMPT, DEL_TASK_BOX_TITLE

    def get_del_row_executor(self, task_ids, task_names, del_title, del_callback) -> DelTaskExecutor:
        return DelTaskExecutor(task_ids, task_names, self.main_window,
                               self.main_window, del_title, del_callback)

    def get_del_prompt_title(self) -> tuple:
        return DEL_TASK_PROMPT, DEL_TASK_BOX_TITLE

    def post_process(self):
        super().post_process()
        # 默认隐藏高级查询
        self.advanced_search_widget.setVisible(False)

        # 填充项目下拉框列表
        fill_project_combobox(self.project_name_combobox)

        # 收集数据
        self.data_dict_type_combobox_dict[DataDictTypeEnum.priority.value[0]] = self.priority_combobox
        self.data_dict_type_combobox_dict[DataDictTypeEnum.task_type.value[0]] = self.task_type_combobox
        self.data_dict_type_combobox_dict[DataDictTypeEnum.demand_person.value[0]] = self.demand_person_combobox
        self.data_dict_type_combobox_dict[DataDictTypeEnum.task_status.value[0]] = self.task_status_combobox
        self.data_dict_type_combobox_dict[DataDictTypeEnum.publish_status.value[0]] = self.publish_status_combobox

        # 填充数据字典下拉框列表
        for data_dict_type, combobox in self.data_dict_type_combobox_dict.items():
            fill_data_dict_combobox(combobox, data_dict_type)

    def add_project_combobox_item(self, project):
        # 提供给外部调用，更新项目名称搜素下拉框，添加值
        add_project_combobox_item(self.project_name_combobox, project)

    def update_project_combobox_item(self, project):
        # 提供给外部调用，更新项目名称搜素下拉框，更新值
        update_project_combobox_item(self.project_name_combobox, project)

    def del_project_combobox_item(self, row_index_list):
        # 提供给外部调用，更新项目名称搜素下拉框，删除值
        for row_index in row_index_list:
            self.project_name_combobox.removeItem(row_index)
        self.reset_project_name_combobox()

    def update_data_dict_combobox(self, data_dict_type_code):
        # 提供给外部调用，更新数据字典搜索下拉框
        update_data_dict_combobox(self.data_dict_type_combobox_dict.get(data_dict_type_code), data_dict_type_code)
