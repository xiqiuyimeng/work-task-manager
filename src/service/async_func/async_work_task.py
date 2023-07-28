# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.system_storage.attachment_sqlite import AttachmentSqlite
from src.service.system_storage.comment_sqlite import CommentSqlite
from src.service.system_storage.publish_info_sqlite import PublishInfoSqlite
from src.service.system_storage.task_sqlite import TaskSqlite, Task
from src.service.util.system_storage_util import transactional
from src.service.util.task_cache_util import add_task_names, update_task_name, del_task_names
from src.view.box.message_box import pop_ok

_author_ = 'luwt'
_date_ = '2023/7/11 17:31'


# ----------------------- 获取任务列表 start ----------------------- #

class ListTaskWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list)

    def do_run(self):
        log.info('开始读取任务列表')
        task_list = TaskSqlite().get_task_list()
        self.success_signal.emit(task_list)
        log.info('读取任务列表成功')

    def get_err_msg(self) -> str:
        return '读取任务列表失败'


class ListTaskExecutor(LoadingMaskThreadExecutor):

    def get_worker(self) -> ListTaskWorker:
        return ListTaskWorker()

# ----------------------- 获取任务列表 end ----------------------- #


# ----------------------- 查询任务详情 start ----------------------- #

class TaskDetailWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(Task)

    def __init__(self, task_id):
        super().__init__()
        self.task_id = task_id

    def do_run(self):
        log.info(f'开始读取任务：{self.task_id}')
        # 读取任务
        task_detail = TaskSqlite().get_task_detail(self.task_id)
        # 读取附件信息
        task_detail.attachment_list = AttachmentSqlite().get_by_task_id(self.task_id)
        # 读取评论信息
        task_detail.comment_list = CommentSqlite().get_by_task_id(self.task_id)
        # 读取发版信息
        task_detail.publish_info_list = PublishInfoSqlite().get_by_task_id(self.task_id)
        self.success_signal.emit(task_detail)
        log.info(f'读取任务成功：{self.task_id}')

    def get_err_msg(self) -> str:
        return f'读取任务失败：{self.task_id}'


class TaskDetailExecutor(LoadingMaskThreadExecutor):

    def __init__(self, task_id, *args):
        self.task_id = task_id
        super().__init__(*args)

    def get_worker(self) -> TaskDetailWorker:
        return TaskDetailWorker(self.task_id)

# ----------------------- 查询任务详情 end ----------------------- #


# ----------------------- 添加任务 start ----------------------- #

class AddTaskWorker(ThreadWorkerABC):
    success_signal = pyqtSignal()

    def __init__(self, task):
        super().__init__()
        self.task = task

    @transactional
    def do_run(self):
        log.info(f'开始添加任务：{self.task.task_name}')
        TaskSqlite().add_task(self.task)
        # 添加附件信息
        if self.task.attachment_list:
            AttachmentSqlite().add_attachment_list(self.task.id, self.task.attachment_list)
        # 添加评论信息
        if self.task.comment_list:
            CommentSqlite().add_comment_list(self.task.id, self.task.comment_list)
        # 添加发版信息
        if self.task.publish_info_list:
            PublishInfoSqlite().add_publish_info_list(self.task.id, self.task.publish_info_list)
        # 更新缓存的任务名称列表
        add_task_names(self.task.task_name)
        self.success_signal.emit()
        log.info(f'添加任务：{self.task.task_name} 成功')

    def get_err_msg(self) -> str:
        return f'添加任务失败：{self.task.task_name}'


class AddTaskExecutor(LoadingMaskThreadExecutor):

    def __init__(self, task, *args):
        self.task = task
        super().__init__(*args)

    def get_worker(self) -> AddTaskWorker:
        return AddTaskWorker(self.task)

    def success_post_process(self, *args):
        pop_ok(f'添加任务成功：{self.task.task_name}', self.error_box_title, self.window)
        super().success_post_process()

# ----------------------- 添加任务 end ----------------------- #


# ----------------------- 编辑任务 start ----------------------- #

class EditTaskWorker(ThreadWorkerABC):
    success_signal = pyqtSignal()

    def __init__(self, task):
        super().__init__()
        self.task = task

    @transactional
    def do_run(self):
        log.info(f'开始编辑任务：{self.task.task_name}')
        # 查询原任务名称
        task_sqlite = TaskSqlite()
        origin_task_name = task_sqlite.get_task_name(self.task.id)
        task_sqlite.update_by_id(self.task)
        # 更新附件信息
        AttachmentSqlite().update_attachment_list(self.task.id, self.task.attachment_list)
        # 更新评论信息
        CommentSqlite().update_comment_list(self.task.id, self.task.comment_list)
        # 更新发版信息
        PublishInfoSqlite().update_publish_info_list(self.task.id, self.task.publish_info_list)
        # 更新缓存中的名称
        update_task_name(origin_task_name, self.task.task_name)
        self.success_signal.emit()
        log.info(f'编辑任务成功：{self.task.task_name}')

    def get_err_msg(self) -> str:
        return f'编辑任务失败：{self.task.task_name}'


class EditTaskExecutor(LoadingMaskThreadExecutor):

    def __init__(self, task, *args):
        self.task = task
        super().__init__(*args)

    def get_worker(self) -> EditTaskWorker:
        return EditTaskWorker(self.task)

    def success_post_process(self, *args):
        pop_ok(f'编辑任务成功：{self.task.task_name}', self.error_box_title, self.window)
        super().success_post_process()

# ----------------------- 编辑任务 end ----------------------- #


# ----------------------- 删除任务 start ----------------------- #

class DelTaskWorker(ThreadWorkerABC):
    success_signal = pyqtSignal()

    def __init__(self, task_ids, task_names):
        super().__init__()
        self.task_ids = task_ids
        self.task_names = task_names

    @transactional
    def do_run(self):
        log.info(f'开始删除任务：{self.task_names}')
        TaskSqlite().delete_by_ids(self.task_ids)
        # 删除附件
        AttachmentSqlite().del_attachment_list(self.task_ids)
        # 删除评论
        CommentSqlite().del_comment_list(self.task_ids)
        # 删除发版信息
        PublishInfoSqlite().del_publish_info_list(self.task_ids)
        # 更新缓存任务名称信息
        del_task_names(self.task_names)
        self.success_signal.emit()
        log.info(f'删除任务成功：{self.task_names}')

    def get_err_msg(self) -> str:
        return f'删除任务失败：{self.task_names}'


class DelTaskExecutor(LoadingMaskThreadExecutor):

    def __init__(self, task_ids, task_names, *args):
        self.task_ids = task_ids
        self.task_names = task_names
        super().__init__(*args)

    def get_worker(self) -> DelTaskWorker:
        return DelTaskWorker(self.task_ids, self.task_names)

# ----------------------- 删除任务 end ----------------------- #
