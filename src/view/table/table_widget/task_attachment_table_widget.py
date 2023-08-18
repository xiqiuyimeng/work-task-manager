# -*- coding: utf-8 -*-
from PyQt6.QtCore import QByteArray, Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QHeaderView, QStyle, QWidget, QVBoxLayout, QLabel, QTableWidgetItem

from src.view.table.table_widget.tool_tip_table_widget import ToolTipTableWidget

_author_ = 'luwt'
_date_ = '2023/8/16 17:50'


class TaskAttachmentTableWidget(ToolTipTableWidget):

    def __init__(self, parent):
        self.parent_dialog_width = parent.parent_dialog.size().width()
        self.parent_layout = parent.layout()
        self.attachment_list = list()
        # 图像宽高
        self.image_width = 120
        self.image_height = 150
        # 记录下一个填充列
        self.next_fill_col = 0
        super().__init__(parent)
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

    def setup_other_ui(self):
        self.horizontalHeader().setHidden(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setColumnCount(self.calculate_table_col_count())

    def calculate_table_col_count(self):
        # 计算表格最大列数，用父对话框的宽度，减去布局中存在的边距（需要计算双倍的，因为父对话框的frame布局 frame_layout 也存在边距，
        # 所以不仅需要计算当前布局 parent_layout）
        margin = (self.parent_layout.contentsMargins().left() + self.parent_layout.spacing()) << 2
        max_col_count = (self.parent_dialog_width - margin) // self.image_width
        # 这里需要考虑单元格内widget的布局宽度，由于默认布局的边距是相同的，所以可以使用当前布局来计算
        cell_widget_margin = max_col_count * (self.parent_layout.contentsMargins().left() << 1)
        # 再次计算列数
        return (self.parent_dialog_width - margin - cell_widget_margin) // self.image_width

    def check_index_valid(self, index):
        return index.isValid()

    def collect_attachment_list(self):
        return self.attachment_list

    def echo_data(self, attachment_list):
        self.attachment_list = attachment_list
        self.render_table()

    def render_table(self):
        if self.rowCount():
            self.clearContents()
            self.setRowCount(0)
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
        self.resizeRowsToContents()

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
        # 设置 tooltip
        attachment_widget.setToolTip(file_name)
        self.add_attachment_cell(attachment_widget)

    def add_attachment_cell(self, attachment_widget):
        # 表格添加一个新的单元格
        row_count, col_count = self.rowCount(), self.columnCount()
        # 插入的行索引应该是行数 - 1
        row_index = row_count - 1
        # 如果表格不存在行，或表格下一个填充列大于实际列时，
        # 那么需要转到下一行，插入新一行
        if row_count == 0 or self.next_fill_col > col_count - 1:
            # 插入一行
            self.insertRow(row_count)
            # 重置
            self.next_fill_col = 0
            # 如果新插入了一行，那么插入的行索引需要 + 1
            row_index += 1

            # 插入新行后，暂时将除了第一列，其余列全部置为不可选中状态
            for col in range(1, self.columnCount()):
                item = QTableWidgetItem()
                self.setItem(row_index, col, item)
                # 不可选中：item.flags() & ~Qt.ItemFlag.ItemIsSelectable
                # 可选中：item.flags() | Qt.ItemFlag.ItemIsSelectable
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)

        if self.next_fill_col:
            # 如果下一个填充列大于0，那么需要清除插入新行时，放置的空item
            self.takeItem(row_index, self.next_fill_col)

        # 填充单元格
        self.setCellWidget(row_index, self.next_fill_col, attachment_widget)
        self.next_fill_col += 1

    def load_attachment_list(self, attachment_list):
        self.attachment_list.extend(attachment_list)
        self.render_table()
        # 加载后，滚动到底部
        self.scrollToBottom()

    def delete_attachment(self):
        attachment_list = self.get_selected_attachment_list()
        if attachment_list:
            for attachment in attachment_list:
                self.attachment_list.remove(attachment)
            # 重新渲染表格
            self.render_table()

    def get_selected_attachment_list(self):
        attachment_list = list()
        for selected_range in self.selectedRanges():
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
                    if self.cellWidget(row, column):
                        # 获取索引
                        index = (row * self.columnCount()) + column
                        attachment_list.append(self.attachment_list[index])
        return attachment_list
