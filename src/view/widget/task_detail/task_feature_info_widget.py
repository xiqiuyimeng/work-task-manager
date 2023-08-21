# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QLabel, QComboBox, QFormLayout

from src.constant.task_constant import PROJECT_NAME_LABEL_TEXT, PROJECT_NAME_PLACEHOLDER_TEXT, PRIORITY_LABEL_TEXT, \
    PRIORITY_PLACEHOLDER_TEXT, TASK_TYPE_LABEL_TEXT, TASK_TYPE_PLACEHOLDER_TEXT, DEMAND_PERSON_LABEL_TEXT, \
    DEMAND_PERSON_PLACEHOLDER_TEXT, TASK_STATUS_LABEL_TEXT, TASK_STATUS_PLACEHOLDER_TEXT, PUBLISH_STATUS_LABEL_TEXT, \
    PUBLISH_STATUS_PLACEHOLDER_TEXT
from src.enum.data_dict_enum import DataDictTypeEnum
from src.view.widget.widget_func import fill_project_combobox, fill_data_dict_combobox, setup_form_combox, \
    get_combobox_data

_author_ = 'luwt'
_date_ = '2023/7/27 15:06'


class TaskFeatureInfoWidget(QWidget):
    data_changed_signal = pyqtSignal()

    def __init__(self):
        self._layout: QFormLayout = ...
        # 项目列表 combobox
        self.project_label: QLabel = ...
        self.project_combobox: QComboBox = ...
        # 优先级列表 combobox
        self.priority_label: QLabel = ...
        self.priority_combobox: QComboBox = ...
        # 任务类型列表 combobox
        self.task_type_label: QLabel = ...
        self.task_type_combobox: QComboBox = ...
        # 需求方列表 combobox
        self.demand_person_label: QLabel = ...
        self.demand_person_combobox: QComboBox = ...
        # 任务状态列表 combobox
        self.task_status_label: QLabel = ...
        self.task_status_combobox: QComboBox = ...
        # 发版状态列表 combobox
        self.publish_status_label: QLabel = ...
        self.publish_status_combobox: QComboBox = ...
        super().__init__()

    def setup_ui(self):
        self._layout = QFormLayout()
        self._layout.setSpacing(20)
        self.setLayout(self._layout)

        self.project_label, self.project_combobox = setup_form_combox(self._layout)
        fill_project_combobox(self.project_combobox)

        self.priority_label, self.priority_combobox = setup_form_combox(self._layout)
        fill_data_dict_combobox(self.priority_combobox, DataDictTypeEnum.priority.value[0])

        self.task_type_label, self.task_type_combobox = setup_form_combox(self._layout)
        fill_data_dict_combobox(self.task_type_combobox, DataDictTypeEnum.task_type.value[0])

        self.demand_person_label, self.demand_person_combobox = setup_form_combox(self._layout)
        fill_data_dict_combobox(self.demand_person_combobox, DataDictTypeEnum.demand_person.value[0])

        self.task_status_label, self.task_status_combobox = setup_form_combox(self._layout)
        fill_data_dict_combobox(self.task_status_combobox, DataDictTypeEnum.task_status.value[0])

        self.publish_status_label, self.publish_status_combobox = setup_form_combox(self._layout)
        fill_data_dict_combobox(self.publish_status_combobox, DataDictTypeEnum.publish_status.value[0])

        self.init_combobox_index()

    def setup_label_text(self):
        self.project_label.setText(PROJECT_NAME_LABEL_TEXT)
        self.project_combobox.setPlaceholderText(PROJECT_NAME_PLACEHOLDER_TEXT)
        self.priority_label.setText(PRIORITY_LABEL_TEXT)
        self.priority_combobox.setPlaceholderText(PRIORITY_PLACEHOLDER_TEXT)
        self.task_type_label.setText(TASK_TYPE_LABEL_TEXT)
        self.task_type_combobox.setPlaceholderText(TASK_TYPE_PLACEHOLDER_TEXT)
        self.demand_person_label.setText(DEMAND_PERSON_LABEL_TEXT)
        self.demand_person_combobox.setPlaceholderText(DEMAND_PERSON_PLACEHOLDER_TEXT)
        self.task_status_label.setText(TASK_STATUS_LABEL_TEXT)
        self.task_status_combobox.setPlaceholderText(TASK_STATUS_PLACEHOLDER_TEXT)
        self.publish_status_label.setText(PUBLISH_STATUS_LABEL_TEXT)
        self.publish_status_combobox.setPlaceholderText(PUBLISH_STATUS_PLACEHOLDER_TEXT)

    def collect_data(self, task):
        get_combobox_data(self.project_combobox, task, 'project_id', 'project_info')
        get_combobox_data(self.priority_combobox, task, 'priority_id', 'priority')
        get_combobox_data(self.task_type_combobox, task, 'task_type_id', 'task_type')
        get_combobox_data(self.demand_person_combobox, task, 'demand_person_id', 'demand_person')
        get_combobox_data(self.task_status_combobox, task, 'status_id', 'status')
        get_combobox_data(self.publish_status_combobox, task, 'publish_status_id', 'publish_status')

    def echo_data(self, task):
        if task.project_info:
            self.project_combobox.setCurrentText(task.project_info.project_name)
        if task.priority:
            self.priority_combobox.setCurrentText(task.priority.dict_name)
        if task.task_type:
            self.task_type_combobox.setCurrentText(task.task_type.dict_name)
        if task.demand_person:
            self.demand_person_combobox.setCurrentText(task.demand_person.dict_name)
        if task.status:
            self.task_status_combobox.setCurrentText(task.status.dict_name)
        if task.publish_status:
            self.publish_status_combobox.setCurrentText(task.publish_status.dict_name)

    def init_combobox_index(self):
        self.project_combobox.setCurrentIndex(-1)
        self.priority_combobox.setCurrentIndex(-1)
        self.task_type_combobox.setCurrentIndex(-1)
        self.demand_person_combobox.setCurrentIndex(-1)
        self.task_status_combobox.setCurrentIndex(-1)
        self.publish_status_combobox.setCurrentIndex(-1)

    def connect_signal(self):
        self.project_combobox.currentIndexChanged.connect(self.project_changed)
        self.priority_combobox.currentIndexChanged.connect(self.data_changed_signal.emit)
        self.task_type_combobox.currentIndexChanged.connect(self.data_changed_signal.emit)
        self.demand_person_combobox.currentIndexChanged.connect(self.data_changed_signal.emit)
        self.task_status_combobox.currentIndexChanged.connect(self.data_changed_signal.emit)
        self.publish_status_combobox.currentIndexChanged.connect(self.data_changed_signal.emit)

    def project_changed(self):
        # 当选择项目时，如果项目中的优先级不为空，联动优先级复选框
        project_info = self.project_combobox.itemData(self.project_combobox.currentIndex())
        if project_info and project_info.priority:
            # 联动优先级复选框后，优先级复选框变化会触发信号，所以不需要发送信号
            self.priority_combobox.setCurrentText(project_info.priority.dict_name)
        else:
            self.data_changed_signal.emit()

    def check_data(self):
        return all((self.project_combobox.currentText(), self.priority_combobox.currentText(),
                    self.task_type_combobox.currentText(), self.demand_person_combobox.currentText(),
                    self.task_status_combobox.currentText(), self.publish_status_combobox.currentText()))
