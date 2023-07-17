# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.system_storage.data_dict_sqlite import DataDictSqlite
from src.service.util.data_dict_cache_util import update_data_dict
from src.view.box.message_box import pop_ok

_author_ = 'luwt'
_date_ = '2023/7/17 17:36'


# ----------------------- 保存数据字典 start ----------------------- #

class SaveDataDictWorker(ThreadWorkerABC):
    success_signal = pyqtSignal()
    
    def __init__(self, data_dict_list):
        super().__init__()
        self.data_dict_list = data_dict_list

    def do_run(self):
        log.info('开始保存数据字典')
        # 持久化到数据库
        DataDictSqlite().save_data_dict(self.data_dict_list)
        # 更新缓存数据
        update_data_dict(self.data_dict_list[0].dict_type, self.data_dict_list)
        self.success_signal.emit()
        log.info('保存数据字典成功')

    def get_err_msg(self) -> str:
        return '保存数据字典失败'


class SaveDataDictExecutor(LoadingMaskThreadExecutor):
    
    def __init__(self, data_dict_list, *args):
        self.data_dict_list = data_dict_list
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return SaveDataDictWorker(self.data_dict_list)

    def success_post_process(self, *args):
        pop_ok('保存数据字典成功', self.error_box_title, self.window)
        super().success_post_process()

# ----------------------- 保存数据字典 end ----------------------- #
