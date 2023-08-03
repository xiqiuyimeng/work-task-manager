# -*- coding: utf-8 -*-
from PyQt6.QtCore import QModelIndex, QAbstractItemModel, Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QItemDelegate, QWidget

from src.view.dialog.color_dialog import ColorDialog, get_rgba_str
from src.view.dialog.table_item_delegate.table_item_input_delegate_dialog import TableItemInputDelegateDialog
from src.view.window.main_window_func import get_window_geometry

_author_ = 'luwt'
_date_ = '2023/7/17 13:44'


class TextInputDelegate(QItemDelegate):

    def __init__(self, duplicate_prompt=None, get_exists_data_list_func=None):
        # 数据重复提示语
        self.duplicate_prompt = duplicate_prompt
        # 获取不重复数据列表的方法
        self.get_exists_data_list_func = get_exists_data_list_func
        self.input_dialog: TableItemInputDelegateDialog = ...
        # 新数据
        self.new_data = ...
        super().__init__()

    def createEditor(self, parent: 'QWidget', option: 'QStyleOptionViewItem', index: QModelIndex) -> QWidget:
        """创建编辑器，只有在编辑时才会触发，编辑器控件选择combox"""
        self.input_dialog = TableItemInputDelegateDialog(index.row() + 1, index.column(),
                                                         bool(self.get_exists_data_list_func),
                                                         self.duplicate_prompt)
        self.input_dialog.setModal(True)
        self.input_dialog.save_signal.connect(self.update_new_data)
        return self.input_dialog

    def update_new_data(self, data):
        self.new_data = data

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        """将模型中的数据，赋值到对话框中"""
        if self.get_exists_data_list_func:
            self.input_dialog.frame.set_exists_data_list(self.get_exists_data_list_func(index.row()))
        self.input_dialog.frame.echo_dialog_data(index.model().data(index))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        """提交对话框的数据到模型中，只要对话框关闭就会触发，所以这里需要判断是否是对话框保存后触发的"""
        if self.new_data is not Ellipsis:
            model.setData(index, self.new_data)
            # 提交数据到模型后，将当前单元格数据重置
            self.new_data = ...

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex):
        """调整文本输入对话框位置"""
        editor.resize_dialog()


class ColorDelegate(QItemDelegate):
    color_changed = pyqtSignal(int, int, str)

    def __init__(self):
        self.new_color = ...
        super().__init__()

    def createEditor(self, parent, option, index):
        editor = ColorDialog(parent)
        # 颜色改变发出信号，方便页面动态渲染颜色
        editor.currentColorChanged.connect(lambda color: self.color_changed_slot(index, color))
        # 最终选择颜色后，更新数据
        editor.colorSelected.connect(self.update_new_data)
        return editor

    def color_changed_slot(self, index, color):
        self.change_color(index, get_rgba_str(color))

    def update_new_data(self, data):
        self.new_color = data

    def setEditorData(self, editor, index):
        value = index.data(Qt.ItemDataRole.EditRole)
        if isinstance(value, QColor):
            editor.setCurrentColor(value)

    def setModelData(self, editor, model, index):
        if self.new_color is not Ellipsis:
            model.setData(index, get_rgba_str(self.new_color))
            # 数据重置
            self.new_color = ...
        else:
            # 获取原来的颜色 重置颜色
            self.change_color(index, index.data())

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex):
        """调整颜色选择对话框位置"""
        window_geometry = get_window_geometry()
        editor.resize(window_geometry.width(), window_geometry.height())

    def change_color(self, index, color_rgba_str):
        self.color_changed.emit(index.row(), index.column(), color_rgba_str)
