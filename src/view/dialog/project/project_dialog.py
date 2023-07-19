# -*- coding: utf-8 -*-
from src.constant.project_constant import PROJECT_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.project.project_dialog_frame import ProjectDialogFrame

_author_ = 'luwt'
_date_ = '2023/7/18 15:03'


class ProjectDialog(CustomDialogABC):
    """项目列表对话框"""

    def __init__(self):
        super().__init__(PROJECT_TITLE)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.6, self.window_geometry.height() * 0.6)

    def get_frame(self) -> ProjectDialogFrame:
        return ProjectDialogFrame(self, self.dialog_title)
