# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QWheelEvent
from PyQt6.QtWidgets import QAbstractScrollArea, QAbstractItemView, QScrollArea, QFrame, QTextBrowser

_author_ = 'luwt'
_date_ = '2023/7/10 14:54'


class ScrollableWidget(QAbstractScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        if hasattr(self, 'setVerticalScrollMode'):
            # 按像素滚动
            self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
            self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            # 如果是按下 shift 键进行鼠标滚轮滚动，执行水平滚动
            scroll_value = 10 if event.angleDelta().y() < 0 else -10
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + scroll_value)
        else:
            super().wheelEvent(event)

    def enterEvent(self, event):
        """设置滚动条在进入控件区域的时候显示"""
        self.verticalScrollBar().setHidden(False)
        self.horizontalScrollBar().setHidden(False)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """设置滚动条在离开控件区域的时候隐藏"""
        self.verticalScrollBar().setHidden(True)
        self.horizontalScrollBar().setHidden(True)
        super().leaveEvent(event)


class ScrollArea(QScrollArea, ScrollableWidget):

    def __init__(self, *args):
        super().__init__(*args)
        # 去除边框
        self.setFrameShape(QFrame.Shape.NoFrame)
        # 设置可以调节控件大小
        self.setWidgetResizable(True)
        # 垂直滚动条策略
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def set_canvas_widget(self, canvas_widget):
        """设置画布部件，滚动区域的原理为：在画布之上进行滚动，像用放大镜看画布一样"""
        self.setWidget(canvas_widget)

    def wheelEvent(self, e: QWheelEvent):
        """如果当前按键为 ctrl + 滚轮，那么跳过，否则会导致滚动和缩放一起进行"""
        if e.modifiers() == Qt.KeyboardModifier.ControlModifier:
            ...
        else:
            ScrollableWidget.wheelEvent(self, e)


class ScrollableZoomWidget(ScrollableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLineWrapMode(self.LineWrapMode.NoWrap)

    def wheelEvent(self, e: QWheelEvent):
        """实现ctrl + 滚轮缩放功能"""
        if e.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if e.angleDelta().y() > 0:
                # 放大
                self.zoomIn()
            else:
                self.zoomOut()
        else:
            ScrollableWidget.wheelEvent(self, e)


class ScrollableTextBrowser(QTextBrowser, ScrollableZoomWidget):
    ...
