# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QFileDialog

from src.constant.task_constant import ADD_ATTACHMENT_BUTTON_TEXT, DOWNLOAD_ATTACHMENT_BUTTON_TEXT, \
    DELETE_ATTACHMENT_BUTTON_TEXT, SELECT_ATTACHMENT_DIALOG_TITLE, LOAD_ATTACHMENT_BOX_TITLE, \
    DOWNLOAD_ATTACHMENT_BOX_TITLE
from src.service.async_func.async_work_task import LoadAttachmentExecutor, DownloadAttachmentExecutor
from src.view.table.table_widget.task_attachment_table_widget import TaskAttachmentTableWidget

_author_ = 'luwt'
_date_ = '2023/8/15 14:51'


class TaskAttachmentInfoWidget(QWidget):

    def __init__(self, parent_dialog):
        self.parent_dialog = parent_dialog
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
        self.table_widget: TaskAttachmentTableWidget = ...

        # 加载附件执行器
        self.load_file_executor: LoadAttachmentExecutor = ...
        # 下载附件执行器
        self.download_file_executor: DownloadAttachmentExecutor = ...
        super().__init__()

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

        self.table_widget = TaskAttachmentTableWidget(self)
        self._layout.addWidget(self.table_widget)

    def setup_label_text(self):
        self.add_button.setText(ADD_ATTACHMENT_BUTTON_TEXT)
        self.download_button.setText(DOWNLOAD_ATTACHMENT_BUTTON_TEXT)
        self.delete_button.setText(DELETE_ATTACHMENT_BUTTON_TEXT)

    def collect_data(self, task):
        task.attachment_list = self.table_widget.collect_attachment_list()

    def echo_data(self, task):
        self.table_widget.echo_data(task.attachment_list)

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
        self.table_widget.load_attachment_list(attachment_list)

    def download_attachment(self):
        attachment_list = self.table_widget.get_selected_attachment_list()
        if attachment_list:
            dir_url = QFileDialog.getExistingDirectory()
            if dir_url:
                self.download_file_executor = DownloadAttachmentExecutor(dir_url, attachment_list,
                                                                         self.parent_dialog,
                                                                         self.parent_dialog,
                                                                         DOWNLOAD_ATTACHMENT_BOX_TITLE)
                self.download_file_executor.start()

    def delete_attachment(self):
        self.table_widget.delete_attachment()
