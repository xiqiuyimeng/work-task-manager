# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.service.system_storage.project_sqlite import Project
from src.view.dialog.custom_dialog_abc import CustomSaveDialogABC
from src.view.frame.project.project_detail_dialog_frame import ProjectDetailDialogFrame

_author_ = 'luwt'
_date_ = '2023/7/18 15:29'


class ProjectDetailDialog(CustomSaveDialogABC):
    """项目详细内容对话框"""
    save_signal = pyqtSignal(Project)
    edit_signal = pyqtSignal(Project)

    def __init__(self, dialog_title, exists_names, project=None):
        self.exists_names = exists_names
        self.project = project
        super().__init__(dialog_title)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.6, self.window_geometry.height() * 0.7)

    def get_frame(self) -> ProjectDetailDialogFrame:
        return ProjectDetailDialogFrame(self, self.dialog_title, self.exists_names, self.project)
