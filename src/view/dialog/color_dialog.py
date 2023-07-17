# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QColorDialog, QPushButton, QDialogButtonBox

_author_ = 'luwt'
_date_ = '2023/7/17 15:09'


class ColorDialog(QColorDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel)
        # 创建清除按钮
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_color)

        button_box = self.findChild(QDialogButtonBox)
        button_box.addButton(self.clear_button, QDialogButtonBox.ButtonRole.ResetRole)

    def clear_color(self):
        self.setCurrentColor(Qt.GlobalColor.transparent)
