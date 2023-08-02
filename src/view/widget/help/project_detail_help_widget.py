# -*- coding: utf-8 -*-
from src.constant.help.project_detail_help_constant import *
from src.view.widget.help import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/8/2 15:21'


class ProjectDetailHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
