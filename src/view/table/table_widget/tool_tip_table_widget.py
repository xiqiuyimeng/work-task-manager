# -*- coding: utf-8 -*-
from PyQt6.QtCore import QEvent, QPoint, Qt
from PyQt6.QtWidgets import QTableWidget, QFrame, QToolTip

from src.view.custom_widget.scrollable_widget import ScrollableWidget

_author_ = 'luwt'
_date_ = '2023/8/16 17:45'


class ToolTipTableWidget(QTableWidget, ScrollableWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signal()
        # 安装监听器
        self.installEventFilter(self)

    def setup_ui(self):
        # 去除选中时虚线框
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # 设置无边框
        self.setFrameShape(QFrame.Shape.NoFrame)
        # 隐藏网格线
        self.setShowGrid(False)
        # 默认行号隐藏
        self.verticalHeader().setHidden(True)

        self.setup_other_ui()

    def setup_other_ui(self):
        ...

    def connect_signal(self):
        # 需要开启鼠标追踪，才能实现tooltip
        self.setMouseTracking(True)
        self.entered.connect(self.show_tool_tip)
        self.connect_other_signal()

    def show_tool_tip(self, model_index):
        self.setToolTip(model_index.data())

    def eventFilter(self, obj, event: QEvent) -> bool:
        if obj == self and event.type() == QEvent.Type.ToolTip:
            # self.indexAt(pos).isValid()，计算规则是默认隐藏了表头，所以需要减去表头高度，才是真实单元格的位置
            horizontal_header_pos = QPoint(0, self.horizontalHeader().height())
            index = self.indexAt(event.pos() - horizontal_header_pos)
            # 索引有效，且索引处部件为空，证明当前是正常的内容单元格，否则为控件单元格
            if index.isValid() and self.indexWidget(index) is None:
                # 设置气泡提示，向下略微偏移一些，以免鼠标挡住提示文字
                QToolTip.showText(QPoint(event.globalPos().x() + 5, event.globalPos().y() + 10), self.toolTip())
            return True
        return super().eventFilter(obj, event)

    def connect_other_signal(self):
        ...
