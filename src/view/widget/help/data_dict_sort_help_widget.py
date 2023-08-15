# -*- coding: utf-8 -*-
from src.constant.help.data_dict_sort_help_constant import *
from src.view.widget.help import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/8/15 10:41'


class DataDictSortHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
