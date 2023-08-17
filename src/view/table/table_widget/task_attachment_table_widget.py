# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QHeaderView

from src.view.table.table_widget.tool_tip_table_widget import ToolTipTableWidget

_author_ = 'luwt'
_date_ = '2023/8/16 17:50'


class TaskAttachmentTableWidget(ToolTipTableWidget):

    def setup_other_ui(self):
        self.horizontalHeader().setHidden(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
