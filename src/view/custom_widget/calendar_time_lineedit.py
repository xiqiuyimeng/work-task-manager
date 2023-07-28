# -*- coding: utf-8 -*-
from datetime import datetime

from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QLineEdit

from src.view.custom_widget.calendar_time_widget import CalendarTimeWidget

_author_ = 'luwt'
_date_ = '2023/7/26 17:11'


class CalendarTimeLineEdit(QLineEdit):

    def __init__(self):
        self.calendar_time_widget: CalendarTimeWidget = ...
        super().__init__()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # 打开日历控件
        self.calendar_time_widget = CalendarTimeWidget()
        # 日历控件，移动到输入框正下方
        start_point = QPoint(self.rect().bottomLeft().x(), self.rect().bottomLeft().y() + 10)
        self.calendar_time_widget.move(self.mapToGlobal(start_point))
        # 日期值回显
        if self.text():
            current_datetime = datetime.strptime(self.text(), '%Y-%m-%d %H:%M')
            self.calendar_time_widget.set_date(current_datetime.date())
            self.calendar_time_widget.set_time(current_datetime.time())
        # 连接信号
        self.calendar_time_widget.date_time_signal.connect(self.setText)
        self.calendar_time_widget.show()

    def keyPressEvent(self, event):
        # 屏蔽所有按键事件，这样就只有通过日历控件才能输入日期数据
        ...
