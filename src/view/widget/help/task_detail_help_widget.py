# -*- coding: utf-8 -*-
from src.constant.help.task_detail_help_constant import *
from src.view.widget.help import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/8/2 15:26'


class TaskDetailHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_label(BASIC_INFO_LABEL_TEXT, BASIC_INFO_HELP_TEXT)
        self.add_row_text_browser(FEATURE_INFO_LABEL_TEXT, FEATURE_INFO_HELP_TEXT)
        self.add_row_text_browser(ATTACHMENT_INFO_LABEL_TEXT, ATTACHMENT_INFO_HELP_TEXT)
        self.add_row_text_browser(PUBLISH_INFO_LABEL_TEXT, PUBLISH_INFO_HELP_TEXT)
