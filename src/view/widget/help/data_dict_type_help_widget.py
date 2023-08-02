# -*- coding: utf-8 -*-
from src.constant.help.data_dict_type_help_constant import *
from src.view.widget.help import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/8/2 10:49'


class DataDictTypeHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_text_browser(DATA_DICT_LIST_LABEL_TEXT, DATA_DICT_LIST_HELP_TEXT)
