# -*- coding: utf-8 -*-
from PyQt6.QtCore import QFile, QIODevice, QTextStream

_author_ = 'luwt'
_date_ = '2023/7/10 12:13'


def read_file(file_path):
    file = QFile(file_path)
    # 确定是读取文本文件，并且自动把换行符修改为 '\n'
    file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
    content = QTextStream(file).readAll()
    file.close()
    return content


def read_qss():
    return read_file("qss:style.qss")
