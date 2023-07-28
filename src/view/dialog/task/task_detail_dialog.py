# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.service.system_storage.task_sqlite import Task
from src.view.dialog.custom_dialog_abc import CustomSaveDialogABC
from src.view.frame.task.task_detail_dialog_frame import TaskDetailDialogFrame

_author_ = 'luwt'
_date_ = '2023/7/26 9:12'


class TaskDetailDialog(CustomSaveDialogABC):
    """任务详情对话框"""
    save_signal = pyqtSignal(Task)
    edit_signal = pyqtSignal(Task)

    def __init__(self, dialog_title, task_id=None):
        self.task_id = task_id
        super().__init__(dialog_title)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.6, self.window_geometry.height() * 0.7)

    def get_frame(self) -> TaskDetailDialogFrame:
        return TaskDetailDialogFrame(self, self.dialog_title, self.task_id)
