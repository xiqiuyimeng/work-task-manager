# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/7/10 13:42'


# 维护主窗口，方便其他窗口使用
main_window = ...


def set_window(window):
    global main_window
    main_window = window


def get_window():
    return main_window


def get_window_geometry():
    return main_window.geometry()
