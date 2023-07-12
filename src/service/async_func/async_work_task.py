# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.system_storage.task_sqlite import TaskSqlite

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

    def get_worker(self) -> ThreadWorkerABC:
        return ListTaskWorker()

# ----------------------- 获取任务列表 end ----------------------- #
