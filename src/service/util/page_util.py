# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List

from src.service.util.dataclass_util import init

_author_ = 'luwt'
_date_ = '2023/7/13 9:15'


@init
@dataclass
class Page:
    # 分页条数
    page_size: int = field(init=False, default=None)
    # 分页页码
    page_no: int = field(init=False, default=None)
    # 总条数
    total_count: int = field(init=False, default=None)
    # 总页数
    total_page: int = field(init=False, default=None)
    # 当前页起始行
    start_row: int = field(init=False, default=None)
    # 当前页结束行
    end_row: int = field(init=False, default=None)
    # 分页数据
    data: List = field(init=False, default=None)

    def init_page(self):
        self.page_size = 10
        self.page_no = 1
        self.total_count = 0
        self.total_page = 1
        return self
