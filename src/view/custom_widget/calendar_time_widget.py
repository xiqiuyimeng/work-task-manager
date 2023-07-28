# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QFormLayout, QLabel, QTimeEdit, QGridLayout, \
    QPushButton

from src.constant.window_constant import SELECT_TIME_LABEL_TEXT, SELECT_TIME_RESULT_LABEL_TEXT, \
    RESET_DATE_TIME_BTN_TEXT, SELECT_DATE_OK_BTN_TEXT, CANCEL_SELECT_DATE_BTN_TEXT

_author_ = 'luwt'
_date_ = '2023/7/26 14:58'


class CalendarTimeWidget(QWidget):
    date_time_signal = pyqtSignal(str)

    def __init__(self):
        self._layout: QVBoxLayout = ...
        self.calendar_widget: QCalendarWidget = ...
        self.form_layout: QFormLayout = ...
        self.time_label: QLabel = ...
        self.time_edit: QTimeEdit = ...
        self.result_label: QLabel = ...
        self.result_value_label: QLabel = ...
        self.button_layout: QGridLayout = ...
        self.day_start_time_button: QPushButton = ...
        self.day_end_time_button: QPushButton = ...
        self.reset_button: QPushButton = ...
        self.ok_button: QPushButton = ...
        self.cancel_button: QPushButton = ...
        super().__init__()

        # 设为模态
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.setup_ui()
        self.setup_label_text()
        self.connect_signal()
        self.post_process()

    def setup_ui(self):
        self._layout = QVBoxLayout(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # 创建日历小部件
        self.calendar_widget = QCalendarWidget()
        self._layout.addWidget(self.calendar_widget)

        self.form_layout = QFormLayout()
        self._layout.addLayout(self.form_layout)
        self.time_label = QLabel()
        self.time_label.setObjectName('form_label')
        # 创建时间编辑小部件
        self.time_edit = QTimeEdit()
        self.form_layout.addRow(self.time_label, self.time_edit)

        self.result_label = QLabel()
        self.result_label.setObjectName('form_label')
        self.result_value_label = QLabel()
        self.form_layout.addRow(self.result_label, self.result_value_label)

        # 按钮组
        self.button_layout = QGridLayout()
        self._layout.addLayout(self.button_layout)
        self.reset_button = QPushButton()
        self.reset_button.setObjectName('reset_button')
        self.button_layout.addWidget(self.reset_button, 0, 0, 1, 1)
        self.ok_button = QPushButton()
        self.ok_button.setObjectName('save_button')
        self.button_layout.addWidget(self.ok_button, 0, 1, 1, 1)
        self.cancel_button = QPushButton()
        self.cancel_button.setObjectName('cancel_button')
        self.button_layout.addWidget(self.cancel_button, 0, 2, 1, 1)

    def setup_label_text(self):
        self.time_label.setText(SELECT_TIME_LABEL_TEXT)
        self.result_label.setText(SELECT_TIME_RESULT_LABEL_TEXT)
        self.reset_button.setText(RESET_DATE_TIME_BTN_TEXT)
        self.ok_button.setText(SELECT_DATE_OK_BTN_TEXT)
        self.cancel_button.setText(CANCEL_SELECT_DATE_BTN_TEXT)

    def connect_signal(self):
        self.calendar_widget.clicked.connect(self.display_date_time)
        self.time_edit.timeChanged.connect(self.display_date_time)
        self.reset_button.clicked.connect(lambda: self.result_value_label.setText(''))
        self.ok_button.clicked.connect(self.save_date_time)
        self.cancel_button.clicked.connect(self.close)

    def display_date_time(self):
        date = self.calendar_widget.selectedDate().toString('yyyy-MM-dd')
        self.result_value_label.setText(f"{date} {self.time_edit.text()}")

    def save_date_time(self):
        self.date_time_signal.emit(self.result_value_label.text())
        self.close()

    def post_process(self):
        self.display_date_time()

    def set_date(self, date):
        self.calendar_widget.setSelectedDate(date)

    def set_time(self, time):
        self.time_edit.setTime(time)
