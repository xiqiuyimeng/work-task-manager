# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt, QByteArray
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QFileDialog, QStyle, QTableWidget, \
    QHeaderView

from src.constant.task_constant import ADD_ATTACHMENT_BUTTON_TEXT, DOWNLOAD_ATTACHMENT_BUTTON_TEXT, \
    DELETE_ATTACHMENT_BUTTON_TEXT, SELECT_ATTACHMENT_DIALOG_TITLE, LOAD_ATTACHMENT_BOX_TITLE, \
    DOWNLOAD_ATTACHMENT_BOX_TITLE
from src.service.async_func.async_work_task import LoadAttachmentExecutor, DownloadAttachmentExecutor

_author_ = 'luwt'
_date_ = '2023/8/15 14:51'


class TaskAttachmentInfoWidget(QWidget):

    def __init__(self, parent_dialog):
        self.parent_dialog = parent_dialog
        self.parent_dialog_width = self.parent_dialog.size().width()
        self._layout: QVBoxLayout = ...
        # 按钮区
        self.button_layout: QGridLayout = ...
        # 添加附件按钮
        self.add_button: QPushButton = ...
        # 下载附件按钮
        self.download_button: QPushButton = ...
        # 删除附件按钮
        self.delete_button: QPushButton = ...
        # 附件展示区
        self.table_widget: QTableWidget = ...
        # 图像宽高
        self.image_width = 120
        self.image_height = 150
        # 记录当前填充到表格的哪一列
        self.table_current_col = 0
        # 附件列表
        self.attachment_list = list()
        # 加载附件执行器
        self.load_file_executor: LoadAttachmentExecutor = ...
        # 下载附件执行器
        self.download_file_executor: DownloadAttachmentExecutor = ...
        super().__init__()
        # 默认文件图片
        self.other_file_pixmap = self.get_other_file_pixmap()

    def get_other_file_pixmap(self):
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
        pixmap = icon.pixmap(self.image_width, self.image_height)
        return self.scale_pixmap(pixmap)

    def scale_pixmap(self, pixmap):
        return pixmap.scaled(self.image_width, self.image_height,
                             aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                             transformMode=Qt.TransformationMode.SmoothTransformation)

    def setup_ui(self):
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self.button_layout = QGridLayout()
        self._layout.addLayout(self.button_layout)

        self.button_layout.addWidget(QLabel(), 0, 0, 1, 2)
        self.add_button = QPushButton()
        self.add_button.setObjectName('add_button')
        self.button_layout.addWidget(self.add_button, 0, 2, 1, 1)
        self.download_button = QPushButton()
        self.download_button.setObjectName('download_button')
        self.button_layout.addWidget(self.download_button, 0, 3, 1, 1)
        self.delete_button = QPushButton()
        self.delete_button.setObjectName('del_button')
        self.button_layout.addWidget(self.delete_button, 0, 4, 1, 1)

        self.table_widget = QTableWidget()
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget.setColumnCount(self.calculate_table_col_count())
        self.table_widget.setShowGrid(False)
        self.table_widget.horizontalHeader().setHidden(True)
        self.table_widget.verticalHeader().setHidden(True)
        self._layout.addWidget(self.table_widget)

    def calculate_table_col_count(self):
        # 计算表格最大列数，用父对话框的宽度，减去布局中存在的边距（需要计算双倍的，因为父对话框的frame布局 frame_layout 也存在边距，
        # 所以不仅需要计算当前控件的布局 _layout）
        margin = (self._layout.contentsMargins().left() + self._layout.spacing()) << 2
        max_col_count = (self.parent_dialog_width - margin) // self.image_width
        # 这里需要考虑单元格内widget的布局宽度，由于默认布局的边距是相同的，所以可以使用当前布局来计算
        cell_widget_margin = max_col_count * (self._layout.contentsMargins().left() << 1)
        # 再次计算列数
        return (self.parent_dialog_width - margin - cell_widget_margin) // self.image_width

    def setup_label_text(self):
        self.add_button.setText(ADD_ATTACHMENT_BUTTON_TEXT)
        self.download_button.setText(DOWNLOAD_ATTACHMENT_BUTTON_TEXT)
        self.delete_button.setText(DELETE_ATTACHMENT_BUTTON_TEXT)

    def collect_data(self, task):
        task.attachment_list = self.attachment_list

    def echo_data(self, task):
        self.attachment_list = task.attachment_list
        self.render_table_widget()

    def render_table_widget(self):
        if self.table_widget.rowCount():
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
        for attachment in self.attachment_list:
            # 加载内容
            bytearray_data = QByteArray(attachment.attachment_content)
            image = QImage()
            image.loadFromData(bytearray_data)
            self.add_attachment(image, attachment.attachment_name)

    def add_attachment(self, image, file_name):
        if image.isNull():
            pixmap = self.other_file_pixmap
        else:
            pixmap = QPixmap.fromImage(self.scale_pixmap(image))
        self.add_attachment_widget(pixmap, file_name)
        # 调整行高度
        self.table_widget.resizeRowsToContents()

    def connect_signal(self):
        self.add_button.clicked.connect(self.open_file_dialog)
        self.download_button.clicked.connect(self.download_attachment)
        self.delete_button.clicked.connect(self.delete_attachment)

    def open_file_dialog(self):
        # 打开文件对话框，选择文件
        file_url = QFileDialog.getOpenFileNames(self, SELECT_ATTACHMENT_DIALOG_TITLE)
        if file_url[0]:
            self.load_file_executor = LoadAttachmentExecutor(file_url[0], self.parent_dialog,
                                                             self.parent_dialog, LOAD_ATTACHMENT_BOX_TITLE,
                                                             self.load_attachment_callback)
            self.load_file_executor.start()

    def load_attachment_callback(self, attachment_list):
        self.attachment_list.extend(attachment_list)
        self.render_table_widget()

    def add_attachment_widget(self, pixmap, file_name):
        # 添加附件，需要两个控件：label 展示附件，label 展示附件名称
        attachment_widget = QWidget()
        attachment_layout = QVBoxLayout(attachment_widget)
        label = QLabel()
        label.setPixmap(pixmap)
        attachment_layout.addWidget(label)
        name_label = QLabel()
        name_label.setText(file_name)
        attachment_layout.addWidget(name_label)
        attachment_layout.setSpacing(0)
        self.add_attachment_cell(attachment_widget)

    def add_attachment_cell(self, attachment_widget):
        # 表格添加一个新的单元格
        row_count, col_count = self.table_widget.rowCount(), self.table_widget.columnCount()
        # 插入的行索引应该是行数 - 1
        row_index = row_count - 1
        # 如果表格不存在行，或表格上次填充列已经是最后一列，即 table_current_col 在上次填充完后，自增1等于列数，
        # 那么需要转到下一行，插入新一行
        if row_count == 0 or self.table_current_col == col_count:
            # 插入一行
            self.table_widget.insertRow(row_count)
            # 重置列
            self.table_current_col = 0
            # 如果新插入了一行，那么插入的行索引需要 + 1
            row_index += 1
        # 填充单元格
        self.table_widget.setCellWidget(row_index, self.table_current_col, attachment_widget)
        self.table_current_col += 1

    def download_attachment(self):
        attachment_list = self.get_selected_attachment_list()
        if attachment_list:
            dir_url = QFileDialog.getExistingDirectory()
            if dir_url:
                self.download_file_executor = DownloadAttachmentExecutor(dir_url, attachment_list,
                                                                         self.parent_dialog,
                                                                         self.parent_dialog,
                                                                         DOWNLOAD_ATTACHMENT_BOX_TITLE)
                self.download_file_executor.start()

    def delete_attachment(self):
        attachment_list = self.get_selected_attachment_list()
        if attachment_list:
            for attachment in attachment_list:
                self.attachment_list.remove(attachment)
            # 重新渲染表格
            self.render_table_widget()

    def get_selected_attachment_list(self):
        attachment_list = list()
        for selected_range in self.table_widget.selectedRanges():
            # 获取范围顶部行索引
            top_row = selected_range.topRow()
            # 获取范围底部行索引
            bottom_row = selected_range.bottomRow()
            # 获取范围左侧列索引
            left_column = selected_range.leftColumn()
            # 获取范围右侧列索引
            right_column = selected_range.rightColumn()

            # 遍历范围内的单元格
            for row in range(top_row, bottom_row + 1):
                for column in range(left_column, right_column + 1):
                    if self.table_widget.cellWidget(row, column):
                        # 获取索引
                        index = (row * self.table_widget.columnCount()) + column
                        attachment_list.append(self.attachment_list[index])
        return attachment_list
