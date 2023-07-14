# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStatusBar

from src.constant.window_constant import WINDOW_TITLE
from src.enum.icon_enum import get_icon
from src.service.util.system_storage_util import close_conn
from src.view.bar.menubar import Menubar
from src.view.bar.titlebar import TitleBar
from src.view.bar.toolbar import ToolBar
from src.view.widget.search_page_table.task_search_page_table_widget import TaskSearchPageTableWidget

_author_ = 'luwt'
_date_ = '2023/7/10 13:43'


class MainWindow(QMainWindow):

    def __init__(self, screen_rect):
        super().__init__()
        # 当前屏幕的分辨率大小
        self.desktop_screen_rect = screen_rect

        # 主控件，用以包含所有内容
        self.main_widget: QWidget = ...
        self.main_layout: QVBoxLayout = ...

        # 任务表格区
        self.task_table_widget: TaskSearchPageTableWidget = ...

        # 菜单栏、标题栏、工具栏、状态栏
        self.menubar: Menubar = ...
        self.titlebar: TitleBar = ...
        self.toolbar: ToolBar = ...
        self.statusbar: QStatusBar = ...

        self.setup_ui()

    def setup_ui(self):
        # 设置窗口无边框，点击任务栏图标，可以实现隐藏和显示
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint
                            | Qt.WindowType.WindowSystemMenuHint | Qt.WindowType.WindowMinimizeButtonHint
                            | Qt.WindowType.WindowMaximizeButtonHint)
        # 按当前分辨率计算窗口大小
        self.resize(self.desktop_screen_rect.width() * 0.6, self.desktop_screen_rect.height() * 0.75)
        # 不透明度
        self.setWindowOpacity(0.95)
        self.setWindowTitle(WINDOW_TITLE)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        # 设置所有间距为0
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.init_bars()

        self.task_table_widget = TaskSearchPageTableWidget(self)

        # 主布局添加所有部件，依次为标题栏、菜单栏、工具栏、承载了实际窗口内容的主控件，将窗口中央控件设置为包含所有的控件
        self.main_layout.addWidget(self.titlebar)
        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.task_table_widget)
        self.setCentralWidget(self.main_widget)

    def init_bars(self):
        # 菜单栏
        self.menubar = Menubar(self)
        self.menubar.setObjectName("menubar")
        self.menubar.fill_menu_bar()

        # 创建标题栏
        self.titlebar = TitleBar(self, self.menubar)
        self.titlebar.setObjectName("titlebar")
        self.titlebar.setFixedWidth(self.width())

        # 工具栏
        self.toolbar = ToolBar(self)
        self.toolbar.fill_tool_bar()

        # 状态栏
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        # 任务栏图标
        self.setWindowIcon(get_icon('window'))

    def resizeEvent(self, event):
        # 在窗口大小变化时，标题栏宽度随之变化
        self.titlebar.setFixedWidth(self.width())
        super().resizeEvent(event)

    def close(self):
        close_conn()
        super().close()

