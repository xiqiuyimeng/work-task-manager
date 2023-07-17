# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import QAbstractItemView

from src.constant.data_dict_dialog_constant import DUPLICATE_DATA_DICT_NAME_PROMPT
from src.constant.table_constant import DATA_DICT_HEADER_LABELS
from src.service.system_storage.data_dict_sqlite import DataDict
from src.view.table.table_item.table_item_delegate import TextInputDelegate, ColorDelegate
from src.view.table.table_widget.custom_table_widget import CustomTableWidget

_author_ = 'luwt'
_date_ = '2023/7/15 12:27'


class DataDictTableWidget(CustomTableWidget):

    def __init__(self, *args):
        self.text_input_delegate: TextInputDelegate = ...
        self.color_delegate: ColorDelegate = ...
        super().__init__(DATA_DICT_HEADER_LABELS, *args, need_operation=False)

    def setup_other_ui(self):
        super().setup_other_ui()
        self.text_input_delegate = TextInputDelegate(DUPLICATE_DATA_DICT_NAME_PROMPT,
                                                     self.get_exists_data_dict_names)
        # 字典名称设置输入编辑代理
        self.setItemDelegateForColumn(1, self.text_input_delegate)
        # 字体颜色、背景色，设置颜色选择器代理
        self.color_delegate = ColorDelegate()
        self.setItemDelegateForColumn(2, self.color_delegate)
        self.setItemDelegateForColumn(3, self.color_delegate)

    def setup_edit_trigger(self):
        # 双击编辑
        self.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)

    def fill_table(self, cols):
        # 断开信号
        self.itemChanged.disconnect()
        super().fill_table(cols)
        # 连接信号
        self.itemChanged.connect(self.data_change)

    def do_fill_row(self, row_index, row_data, fill_create_time=True):
        self.setItem(row_index, 1, self.make_item(row_data.dict_name, row_data.font_color,
                                                  row_data.background_color))
        self.setItem(row_index, 2, self.make_item(row_data.font_color))
        self.setItem(row_index, 3, self.make_item(row_data.background_color))

    def show_tool_tip(self, model_index):
        if isinstance(model_index.data(), QColor):
            # 展示颜色名称
            self.setToolTip(model_index.data().name())
        else:
            super().show_tool_tip(model_index)

    def connect_other_signal(self):
        # 单行数据变化时，触发
        self.itemChanged.connect(self.data_change)
        # 颜色变化时触发
        self.color_delegate.color_changed.connect(self.dynamic_render_color)

    def data_change(self, item):
        check_num_widget = self.cellWidget(item.row(), 0)
        order_item = check_num_widget.check_label
        data = order_item.row_data
        if item.column() == 1:
            data.dict_name = item.text()
        elif item.column() == 2:
            self.handle_color_change(item)
            data.font_color = item.text()
        elif item.column() == 3:
            self.handle_color_change(item)
            data.background_color = item.text()

    def handle_color_change(self, item):
        color = QColor(item.text())
        if color == Qt.GlobalColor.transparent:
            item.setData(Qt.ItemDataRole.EditRole, None)
        self.dynamic_render_color(item.row(), item.column(), color)

    def dynamic_render_color(self, row, col, color):
        # 断开信号
        self.itemChanged.disconnect()
        # 动态渲染颜色
        if col == 2:
            if color == Qt.GlobalColor.transparent:
                self.item(row, 1).setData(Qt.ItemDataRole.ForegroundRole, None)
            else:
                self.item(row, 1).setForeground(QBrush(color))
        elif col == 3:
            if color == Qt.GlobalColor.transparent:
                self.item(row, 1).setData(Qt.ItemDataRole.BackgroundRole, None)
            else:
                self.item(row, 1).setBackground(QBrush(color))
        # 连接信号
        self.itemChanged.connect(self.data_change)

    def add_new_data_dict(self, data_dict_type):
        data_dict = DataDict()
        data_dict.dict_type = data_dict_type
        # 断开信号
        self.itemChanged.disconnect()
        super().add_row(data_dict)
        # 连接信号
        self.itemChanged.connect(self.data_change)
        # 触发编辑模式
        self.editItem(self.item(self.rowCount() - 1, 1))

    def sync_default_data_dict(self, data_dict_type):
        # 断开信号
        self.itemChanged.disconnect()
        # 获取当前表格已存在的值列表
        exists_data_dict_names = self.get_exists_data_dict_names()
        # 获取当前类型默认值列表
        for data_dict_name in data_dict_type[2]:
            if data_dict_name not in exists_data_dict_names:
                data_dict = DataDict()
                data_dict.dict_name = data_dict_name
                data_dict.dict_type = data_dict_type[0]
                self.add_row(data_dict)
        # 连接信号
        self.itemChanged.connect(self.data_change)

    def get_exists_data_dict_names(self, index=-1):
        return [self.item(row, 1).text() for row in range(self.rowCount()) if row != index]

    def collect_data(self):
        return [self.get_row_data(row) for row in range(self.rowCount())]

    def get_row_data(self, row):
        # 收集数据
        check_num_widget = self.cellWidget(row, 0)
        order_item = check_num_widget.check_label
        return order_item.row_data
