# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QLabel, QPushButton, QComboBox, QGridLayout, QFormLayout

from src.constant.help_constant import PROJECT_DETAIL_HELP
from src.constant.project_constant import PROJECT_NAME_LABEL_TXT, FONT_COLOR_LABEL_TXT, BACKGROUND_COLOR_LABEL_TXT, \
    PRIORITY_LABEL_TXT, PROJECT_DESC_LABEL_TXT, OPEN_FONT_COLOR_DIALOG_BTN_TXT, OPEN_BACKGROUND_COLOR_DIALOG_BTN_TXT, \
    PRIORITY_COMBOBOX_PLACEHOLDER_TEXT, FONT_COLOR_TYPE, BACKGROUND_COLOR_TYPE, PROJECT_NAME_DISPLAY_LABEL_TXT, \
    EDIT_PROJECT_BOX_TITLE, ADD_PROJECT_BOX_TITLE
from src.enum.data_dict_enum import DataDictTypeEnum
from src.service.async_func.async_project_task import AddProjectExecutor, EditProjectExecutor
from src.service.system_storage.project_sqlite import Project
from src.service.util.data_dict_cache_util import get_data_dict_list
from src.view.custom_widget.text_editor import TextEditor
from src.view.dialog.color_dialog import ColorDialog, get_rgba_str, get_color_from_rgba_str
from src.view.frame.name_check_dialog_frame import NameCheckDialogFrame
from src.view.window.main_window_func import get_window

_author_ = 'luwt'
_date_ = '2023/7/18 15:17'


class ProjectDetailDialogFrame(NameCheckDialogFrame):
    """项目详细内容对话框框架"""
    save_signal = pyqtSignal(Project)
    edit_signal = pyqtSignal(Project)

    def __init__(self, parent_dialog, dialog_title, exists_names, project=None):
        self.dialog_data: Project = ...
        self.new_dialog_data: Project = ...
        # 彩色名称展示label
        self.name_display_label: QLabel = ...
        self.name_value_display_label: QLabel = ...
        # 选择字体颜色控件布局
        self.color_layout: QGridLayout = ...
        self.font_color_label: QLabel = ...
        self.font_color_value_label: QLabel = ...
        self.pick_font_color_button: QPushButton = ...

        self.background_color_label: QLabel = ...
        self.background_color_value_label: QLabel = ...
        self.pick_background_color_button: QPushButton = ...

        self.color_dialog: ColorDialog = ...

        self.form_layout: QFormLayout = ...
        # 优先级选择框
        self.priority_label: QLabel = ...
        self.priority_combobox: QComboBox = ...
        # 详细描述
        self.project_desc_label: QLabel = ...
        self.project_desc_text_edit: TextEditor = ...

        # 添加项目执行器
        self.add_project_executor: AddProjectExecutor = ...
        # 编辑项目执行器
        self.edit_project_executor: EditProjectExecutor = ...
        super().__init__(parent_dialog, dialog_title, exists_names, project, read_storage=False)

    def get_new_dialog_data(self) -> Project:
        return Project()

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_other_content_ui(self):
        self.name_display_label = QLabel()
        self.name_display_label.setObjectName('form_label')
        self.name_value_display_label = QLabel()
        self.name_layout.addRow(self.name_display_label, self.name_value_display_label)

        # 创建颜色选择器
        self.color_layout = QGridLayout()
        self.frame_layout.addLayout(self.color_layout)

        self.font_color_label = QLabel()
        self.font_color_label.setObjectName('form_label')
        self.color_layout.addWidget(self.font_color_label, 0, 0, 1, 1)
        self.font_color_value_label = QLabel()
        self.color_layout.addWidget(self.font_color_value_label, 0, 1, 1, 1)
        self.pick_font_color_button = QPushButton()
        self.color_layout.addWidget(self.pick_font_color_button, 0, 2, 1, 1)

        self.background_color_label = QLabel()
        self.background_color_label.setObjectName('form_label')
        self.color_layout.addWidget(self.background_color_label, 0, 3, 1, 1)
        self.background_color_value_label = QLabel()
        self.color_layout.addWidget(self.background_color_value_label, 0, 4, 1, 1)
        self.pick_background_color_button = QPushButton()
        self.color_layout.addWidget(self.pick_background_color_button, 0, 5, 1, 1)

        self.form_layout = QFormLayout()
        self.frame_layout.addLayout(self.form_layout)
        self.priority_label = QLabel()
        self.priority_label.setObjectName('form_label')
        self.priority_combobox = QComboBox()
        self.form_layout.addRow(self.priority_label, self.priority_combobox)

        self.project_desc_label = QLabel()
        self.project_desc_label.setObjectName('form_label')
        self.project_desc_text_edit = TextEditor()
        self.form_layout.addRow(self.project_desc_label, self.project_desc_text_edit)

    def setup_other_label_text(self):
        self.name_label.setText(PROJECT_NAME_LABEL_TXT)
        self.name_display_label.setText(PROJECT_NAME_DISPLAY_LABEL_TXT)
        self.font_color_label.setText(FONT_COLOR_LABEL_TXT)
        self.background_color_label.setText(BACKGROUND_COLOR_LABEL_TXT)
        self.priority_label.setText(PRIORITY_LABEL_TXT)
        self.project_desc_label.setText(PROJECT_DESC_LABEL_TXT)

        self.pick_font_color_button.setText(OPEN_FONT_COLOR_DIALOG_BTN_TXT)
        self.pick_background_color_button.setText(OPEN_BACKGROUND_COLOR_DIALOG_BTN_TXT)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        return PROJECT_DETAIL_HELP

    def collect_input(self):
        self.new_dialog_data.project_name = self.name_input.text()
        self.new_dialog_data.font_color = self.font_color_value_label.text()
        self.new_dialog_data.background_color = self.background_color_value_label.text()
        index = self.priority_combobox.currentIndex()
        if index >= 0:
            self.new_dialog_data.priority = self.priority_combobox.itemData(index)
            self.new_dialog_data.priority_id = self.new_dialog_data.priority.id
        self.new_dialog_data.project_desc = self.project_desc_text_edit.toPlainText()

    def button_available(self) -> bool:
        return self.name_input.displayText() and self.name_available

    def check_data_changed(self) -> bool:
        return self.dialog_data != self.new_dialog_data

    def connect_child_signal(self):
        self.name_input.textEdited.connect(self.name_value_display_label.setText)
        self.pick_font_color_button.clicked.connect(lambda: self.pick_color(FONT_COLOR_TYPE))
        self.pick_background_color_button.clicked.connect(lambda: self.pick_color(BACKGROUND_COLOR_TYPE))
        self.priority_combobox.currentIndexChanged.connect(self.check_input)
        self.project_desc_text_edit.textChanged.connect(self.check_input)

    def pick_color(self, color_type):
        self.color_dialog = ColorDialog()
        # 颜色改变发出信号，方便页面动态渲染颜色
        self.color_dialog.currentColorChanged.connect(lambda color: self.dynamic_render_color(color_type, color))
        # 最终选择颜色后，更新数据
        self.color_dialog.colorSelected.connect(lambda color: self.change_color(color_type, color))
        # 如果点了取消，那么重置颜色
        if self.color_dialog.exec() == ColorDialog.DialogCode.Rejected:
            self.reset_color(color_type)

    def reset_color(self, color_type):
        if color_type == FONT_COLOR_TYPE:
            origin_color = get_color_from_rgba_str(self.font_color_value_label.text())
        else:
            # 背景色特殊处理，如果原来背景色为空，那么重置为透明
            if self.background_color_value_label.text():
                origin_color = get_color_from_rgba_str(self.background_color_value_label.text())
            else:
                origin_color = Qt.GlobalColor.transparent
        self.dynamic_render_color(color_type, origin_color)

    def dynamic_render_color(self, color_type, color: QColor):
        palette = self.name_value_display_label.palette()
        if color_type == FONT_COLOR_TYPE:
            if color == Qt.GlobalColor.transparent:
                color = palette.color(QPalette.ColorRole.WindowText)
            palette.setColor(QPalette.ColorRole.WindowText, color)
        else:
            # 设置背景颜色
            palette.setColor(QPalette.ColorRole.Window, color)
            self.name_value_display_label.setAutoFillBackground(True)
        self.name_value_display_label.setPalette(palette)

    def change_color(self, color_type, color: QColor):
        if color_type == FONT_COLOR_TYPE:
            self.font_color_value_label.setText(get_rgba_str(color))
        else:
            self.background_color_value_label.setText(get_rgba_str(color))
        self.check_input()

    def save_func(self):
        # 原数据存在，说明是编辑
        if self.dialog_data:
            self.new_dialog_data.id = self.dialog_data.id
            self.edit_project_executor = EditProjectExecutor(self.new_dialog_data, self.parent_dialog,
                                                             self.parent_dialog, EDIT_PROJECT_BOX_TITLE,
                                                             self.edit_callback)
            self.edit_project_executor.start()
        else:
            self.add_project_executor = AddProjectExecutor(self.new_dialog_data, self.parent_dialog,
                                                           self.parent_dialog, ADD_PROJECT_BOX_TITLE,
                                                           self.add_callback)
            self.add_project_executor.start()

    def edit_callback(self):
        self.edit_signal.emit(self.new_dialog_data)
        # 更新主界面搜索下拉框，更新数据
        task_table_widget = get_window().task_table_widget
        task_table_widget.update_project_combobox_item(self.new_dialog_data)
        # 更新任务列表数据
        task_table_widget.search()
        self.parent_dialog.close()

    def add_callback(self):
        self.save_signal.emit(self.new_dialog_data)
        # 更新主界面搜索下拉框，添加数据
        task_table_widget = get_window().task_table_widget
        task_table_widget.add_project_combobox_item(self.new_dialog_data)
        # 更新任务列表数据
        task_table_widget.search()
        self.parent_dialog.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        # 暂时屏蔽信号
        self.priority_combobox.blockSignals(True)
        # 填充优先级下拉框
        for priority in get_data_dict_list(DataDictTypeEnum.priority.value[0]):
            self.priority_combobox.addItem(priority.dict_name, priority)
        self.priority_combobox.setMaximumWidth(self.parent_dialog.width() >> 1)
        self.priority_combobox.setCurrentIndex(-1)
        # 恢复信号
        self.priority_combobox.blockSignals(False)
        super().post_process()
        # 动态渲染颜色
        self.reset_color(FONT_COLOR_TYPE)
        self.reset_color(BACKGROUND_COLOR_TYPE)

    def setup_other_placeholder_text(self):
        self.priority_combobox.setPlaceholderText(PRIORITY_COMBOBOX_PLACEHOLDER_TEXT)

    def get_old_name(self) -> str:
        return self.dialog_data.project_name

    def setup_echo_other_data(self):
        self.name_value_display_label.setText(self.dialog_data.project_name)
        self.font_color_value_label.setText(self.dialog_data.font_color)
        self.background_color_value_label.setText(self.dialog_data.background_color)
        if self.dialog_data.priority:
            self.priority_combobox.setCurrentText(self.dialog_data.priority.dict_name)
        self.project_desc_text_edit.setPlainText(self.dialog_data.project_desc)

    # ------------------------------ 后置处理 end ------------------------------ #
