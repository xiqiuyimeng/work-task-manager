# -*- coding: utf-8 -*-
import threading

from PyQt6.QtCore import QThread, pyqtSignal, QObject
from PyQt6.QtGui import QMovie

from src.exception.exception import ThreadStopException
from src.logger.log import logger as log
from src.service.util.system_storage_util import release_connection, set_thread_terminate
from src.view.box.message_box import pop_fail
from src.view.custom_widget.loading_widget import LoadingMaskWidget

_author_ = 'luwt'
_date_ = '2023/7/10 12:29'


# ----------------------- thread worker ABC -----------------------


class ThreadWorkerABC(QThread):
    """异步工作任务基类，定义最基本工作流程"""

    success_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # 标识是否在进行 数据库相关任务
        self.modifying_db_task = False
        self.thread_id = ...

    def run(self):
        try:
            self.thread_id = threading.get_ident()
            self.do_run()
        except Exception as e:
            # 如果是自定义的停止线程异常，那么不需要处理异常，其他异常再进行异常处理
            if not isinstance(e, ThreadStopException):
                self.do_exception(e)
        finally:
            # 清理数据库连接资源
            release_connection()
            self.do_finally()

    def do_run(self):
        ...

    def do_exception(self, e: Exception):
        err_msg = self.get_err_msg()
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e}')

    def get_err_msg(self) -> str:
        ...

    def do_finally(self):
        ...


# ----------------------- thread worker manager ABC -----------------------


class ThreadExecutorABC(QObject):
    """对应 ThreadWorkerABC 设定，负责管理调度异步任务，与view交互工作"""

    def __init__(self, window, error_box_title, success_callback=None, fail_callback=None):
        super().__init__()
        self.window = window
        self.error_box_title = error_box_title
        # 执行成功的回调函数
        self.success_callback = success_callback
        # 执行失败的回调函数
        self.fail_callback = fail_callback

        # 异步任务开始前的准备工作
        self.pre_process()
        # 自定义线程工作对象
        self.worker = self.get_worker()
        # 获取成功失败信息
        self.worker.success_signal.connect(lambda *args: self.success(*args))
        self.worker.error_signal.connect(lambda error_msg: self.fail(error_msg))

    def start(self):
        self.worker.start()

    def success(self, *args):
        self.post_process()
        self.success_post_process(*args)

    def fail(self, error_msg):
        self.post_process()
        self.fail_post_process()
        pop_fail(error_msg, self.error_box_title, self.window)

    def worker_terminate(self, terminate_callback=None):
        if self.worker.isRunning():
            # 如果线程正在处理数据库操作，那么应当抛出异常，使线程中的事务回滚，不产生脏数据
            if self.worker.modifying_db_task:
                # 修改线程内使用连接的标志位，抛出异常，使线程任务结束
                set_thread_terminate(self.worker.thread_id, True)
            else:
                # 如果是普通任务，那么直接停止线程
                self.worker.terminate()
                self.worker.wait()
        # 停止后，首先调用回调函数
        if terminate_callback:
            terminate_callback()
        self.post_process()

    def pre_process(self):
        """前置处理，异步任务开始前的一些准备工作"""
        ...

    def get_worker(self) -> ThreadWorkerABC:
        ...

    def post_process(self):
        """通用后置处理，任务结束后的一些通用工作"""
        ...

    def success_post_process(self, *args):
        if self.success_callback:
            self.success_callback(*args)

    def fail_post_process(self):
        if self.fail_callback:
            self.fail_callback()


# ----------------------- loading mask thread worker manager ABC -----------------------


class LoadingMaskThreadExecutor(ThreadExecutorABC):
    """使用遮罩层作为任务开始时前置动作的调度器"""

    def __init__(self, masked_widget, *args, **kwargs):
        self.loading_movie = QMovie("gif:loading.gif")
        self.masked_widget = masked_widget
        self.loading_mask = LoadingMaskWidget(self.masked_widget, self.loading_movie)
        super().__init__(*args, **kwargs)

    def pre_process(self):
        self.loading_mask.start()

    def post_process(self):
        self.loading_mask.stop()
