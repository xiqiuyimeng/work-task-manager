# -*- coding: utf-8 -*-
from src.constant.help.data_dict_bind_help_constant import *
from src.view.widget.help import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/8/2 14:55'


class DataDictBindHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
