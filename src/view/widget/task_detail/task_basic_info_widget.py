# -*- coding: utf-8 -*-
from datetime import datetime

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel

from src.constant.task_constant import START_TIME_LABEL_TEXT, START_TIME_PLACEHOLDER_TEXT, END_TIME_LABEL_TEXT, \
    END_TIME_PLACEHOLDER_TEXT, TIME_DURATION_LABEL_TEXT, DETAIL_DESC_LABEL_TEXT
from src.constant.window_constant import CALENDAR_FORMATTER
from src.view.custom_widget.calendar_time_lineedit import CalendarTimeLineEdit
from src.view.custom_widget.text_editor import TextEditor

_author_ = 'luwt'
_date_ = '2023/7/27 14:46'


class TaskBasicInfoWidget(QWidget):

    def __init__(self):
        self._layout: QVBoxLayout = ...
        self.time_layout: QHBoxLayout = ...
        self.start_time_layout: QFormLayout = ...
        self.start_time_label: QLabel = ...
        self.start_time_lineedit: CalendarTimeLineEdit = ...
        self.end_time_layout: QFormLayout = ...
        self.end_time_label: QLabel = ...
        self.end_time_lineedit: CalendarTimeLineEdit = ...
        self.time_duration_layout: QFormLayout = ...
        self.time_duration_label: QLabel = ...
        self.time_duration_value_label: QLabel = ...
        self.detail_desc_layout: QFormLayout = ...
        self.detail_desc_label: QLabel = ...
        self.detail_desc_text_edit: TextEditor = ...
        super().__init__()

    def setup_ui(self, name_layout):
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._layout.addLayout(name_layout)

        # 开始时间、结束时间、耗时
        self.time_layout = QHBoxLayout()
        self._layout.addLayout(self.time_layout)
        self.start_time_layout = QFormLayout()
        self.time_layout.addLayout(self.start_time_layout)
        self.start_time_label = QLabel()
        self.start_time_label.setObjectName('form_label')
        self.start_time_lineedit = CalendarTimeLineEdit()
        self.start_time_layout.addRow(self.start_time_label, self.start_time_lineedit)

        self.end_time_layout = QFormLayout()
        self.time_layout.addLayout(self.end_time_layout)
        self.end_time_label = QLabel()
        self.end_time_label.setObjectName('form_label')
        self.end_time_lineedit = CalendarTimeLineEdit()
        self.end_time_layout.addRow(self.end_time_label, self.end_time_lineedit)

        self.time_duration_layout = QFormLayout()
        self.time_layout.addLayout(self.time_duration_layout)
        self.time_duration_label = QLabel()
        self.time_duration_label.setObjectName('form_label')
        self.time_duration_value_label = QLabel()
        self.time_duration_layout.addRow(self.time_duration_label, self.time_duration_value_label)

        self.time_layout.setStretch(0, 2)
        self.time_layout.setStretch(1, 2)
        self.time_layout.setStretch(2, 1)

        # 详细说明
        self.detail_desc_layout = QFormLayout()
        self._layout.addLayout(self.detail_desc_layout)
        self.detail_desc_label = QLabel()
        self.detail_desc_label.setObjectName('form_label')
        self.detail_desc_text_edit = TextEditor()
        self.detail_desc_layout.addRow(self.detail_desc_label, self.detail_desc_text_edit)

    def setup_label_text(self):
        self.start_time_label.setText(START_TIME_LABEL_TEXT)
        self.start_time_lineedit.setPlaceholderText(START_TIME_PLACEHOLDER_TEXT)
        self.end_time_label.setText(END_TIME_LABEL_TEXT)
        self.end_time_lineedit.setPlaceholderText(END_TIME_PLACEHOLDER_TEXT)
        self.time_duration_label.setText(TIME_DURATION_LABEL_TEXT)
        self.detail_desc_label.setText(DETAIL_DESC_LABEL_TEXT)

    def collect_data(self, task):
        task.start_time = self.start_time_lineedit.text()
        task.end_time = self.end_time_lineedit.text()
        task.time_duration = self.time_duration_value_label.text()
        task.content = self.detail_desc_text_edit.toPlainText()

    def echo_data(self, task):
        self.start_time_lineedit.setText(task.start_time)
        self.end_time_lineedit.setText(task.end_time)
        self.time_duration_value_label.setText(task.time_duration)
        self.detail_desc_text_edit.setPlainText(task.content)

    def connect_signal(self):
        self.start_time_lineedit.textChanged.connect(self.calculate_time_duration)
        self.end_time_lineedit.textChanged.connect(self.calculate_time_duration)

    def calculate_time_duration(self):
        # 当开始时间和结束时间都存在时，计算耗时
        if self.start_time_lineedit.text() and self.end_time_lineedit.text():
            start_time = datetime.strptime(self.start_time_lineedit.text(), CALENDAR_FORMATTER)
            end_time = datetime.strptime(self.end_time_lineedit.text(), CALENDAR_FORMATTER)
            time_duration = end_time - start_time
            diff_days = time_duration.days
            diff_minutes = time_duration.seconds // 60
            diff_hours = diff_minutes // 60
            self.time_duration_value_label.setText(f'{diff_days} 天 {diff_hours} 时 {diff_minutes} 分')
