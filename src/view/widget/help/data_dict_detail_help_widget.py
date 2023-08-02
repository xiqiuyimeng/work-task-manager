# -*- coding: utf-8 -*-
from src.constant.help.data_dict_detail_help_constant import *
from src.view.widget.help import HelpWidgetABC

_author_ = 'luwt'
_date_ = '2023/8/2 10:50'


class DataDictDetailHelpWidget(HelpWidgetABC):

    def add_content(self):
        self.add_label(OVERVIEW_TEXT)
        self.add_row_text_browser(DATA_DICT_DETAIL_LABEL_TEXT, DATA_DICT_DETAIL_HELP_TEXT)
        self.add_row_text_browser(COLOR_DIALOG_LABEL_TEXT, COLOR_DIALOG_HELP_TEXT)
