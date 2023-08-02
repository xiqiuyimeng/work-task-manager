# -*- coding: utf-8 -*-
from src.constant.help.project_table_help_constant import *
from src.view.widget.help import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/8/2 15:12'


class ProjectTableHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
