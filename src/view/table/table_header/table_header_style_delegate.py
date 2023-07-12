# -*- coding: utf-8 -*-
from PyQt6.QtCore import QModelIndex
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtWidgets import QStyledItemDelegate

_author_ = 'luwt'
_date_ = '2023/7/10 15:22'


class TableHeaderStyleDelegate(QStyledItemDelegate):

    def paint(self, painter: QPainter, option: 'QStyleOptionViewItem', index: QModelIndex):
        # 绘制背景
        color = QColor(231, 238, 251)
        painter.setPen(color)
        painter.setBrush(QBrush(color))
        painter.drawRect(option.rect)
        super().paint(painter, option, index)
