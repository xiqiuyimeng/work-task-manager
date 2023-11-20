# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.enum.data_dict_enum import DataDictTypeEnum
from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.system_storage.data_dict_sqlite import DataDictSqlite
from src.service.system_storage.project_sqlite import ProjectSqlite
from src.service.system_storage.publish_info_sqlite import PublishInfoSqlite
from src.service.system_storage.task_sqlite import TaskSqlite
from src.service.util.data_dict_cache_util import update_data_dict
from src.service.util.project_cache_util import update_project_priority
from src.service.util.system_storage_util import transactional
from src.view.box.message_box import pop_ok

_author_ = 'luwt'
_date_ = '2023/7/17 17:36'


operate_business_dict = {
    # 优先级
    DataDictTypeEnum.priority.value[0]: {
        'update': (
            ProjectSqlite().update_priority_ids,
            # 更新缓存的项目数据
            update_project_priority,
            TaskSqlite().update_priority_ids
        ),
        'query': (
            # 查询项目中是否绑定数据
            ProjectSqlite().get_used_priority_ids,
            # 查询任务中是否绑定数据
            TaskSqlite().get_used_priority_ids
        )
    },
    # 任务类型
    DataDictTypeEnum.task_type.value[0]: {
        'update': (TaskSqlite().update_task_type_ids, ),
        'query': (TaskSqlite().get_used_task_type_ids, )
    },
    # 需求方
    DataDictTypeEnum.demand_person.value[0]: {
        'update': (TaskSqlite().update_demand_person_ids, ),
        'query': (TaskSqlite().get_used_demand_person_ids, )
    },
    # 任务状态
    DataDictTypeEnum.task_status.value[0]: {
        'update': (TaskSqlite().update_task_status_ids, ),
        'query': (TaskSqlite().get_used_task_status_ids, )
    },
    # 发版状态
    DataDictTypeEnum.publish_status.value[0]: {
        'update': (TaskSqlite().update_publish_status_ids, ),
        'query': (TaskSqlite().get_used_publish_status_ids, )
    },
    # 发版信息类型
    DataDictTypeEnum.publish_type.value[0]: {
        'update': (PublishInfoSqlite().update_publish_type_ids, ),
        'query': (PublishInfoSqlite().get_used_publish_type_ids, )
    }
}


# ----------------------- 保存数据字典 start ----------------------- #

class SaveDataDictWorker(ThreadWorkerABC):
    success_signal = pyqtSignal()
    
    def __init__(self, data_dict_type_code, data_dict_list):
        super().__init__()
        self.data_dict_type_code = data_dict_type_code
        self.data_dict_list = data_dict_list

    @transactional
    def do_run(self):
        log.info('开始保存数据字典')
        # 持久化到数据库
        DataDictSqlite().save_data_dict(self.data_dict_list)
        # 更新缓存数据
        dict_dict = {data_dict.id: data_dict for data_dict in self.data_dict_list}
        update_data_dict(self.data_dict_list[0].dict_type, dict_dict)
        # 更新业务数据
        self.update_business_data()
        self.success_signal.emit()
        log.info('保存数据字典成功')

    def update_business_data(self):
        # 更新业务数据
        for data_dict in self.data_dict_list:
            if data_dict.bind_data_list:
                operate_business_func_dict = operate_business_dict.get(self.data_dict_type_code)
                for update_func in operate_business_func_dict.get('update'):
                    update_func(data_dict.id, [origin_data.id for origin_data in data_dict.bind_data_list])

    def get_err_msg(self) -> str:
        return '保存数据字典失败'


class SaveDataDictExecutor(LoadingMaskThreadExecutor):
    
    def __init__(self, data_dict_type_code, data_dict_list, *args):
        self.data_dict_type_code = data_dict_type_code
        self.data_dict_list = data_dict_list
        super().__init__(*args)

    def get_worker(self) -> SaveDataDictWorker:
        return SaveDataDictWorker(self.data_dict_type_code, self.data_dict_list)

    def success_post_process(self, *args):
        pop_ok('保存数据字典成功', self.error_box_title, self.window)
        super().success_post_process()

# ----------------------- 保存数据字典 end ----------------------- #


# ----------------------- 查询数据字典是否关联数据 start ----------------------- #

class QueryDataDictBindDataWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list)

    def __init__(self, data_dict_type_code, data_dict_ids):
        super().__init__()
        self.data_dict_type_code = data_dict_type_code
        self.data_dict_ids = data_dict_ids

    def do_run(self):
        log.info('开始查询数据字典是否绑定数据')
        # 查询各个数据字典类型，是否存在已绑定的数据，收集所有绑定数据的字典项id
        bind_data_id_list = list()
        operate_business_func_dict = operate_business_dict.get(self.data_dict_type_code)
        for query_func in operate_business_func_dict.get('query'):
            bind_data_id_list.extend(query_func(self.data_dict_ids))
        # 在查询完成后，发射已查到的数据
        self.success_signal.emit(bind_data_id_list)
        log.info('查询数据字典是否绑定数据成功')

    def get_err_msg(self) -> str:
        return '查询数据字典是否绑定数据失败'


class QueryDataDictBindDataExecutor(LoadingMaskThreadExecutor):

    def __init__(self, data_dict_type_code, data_dict_ids, *args):
        self.data_dict_type_code = data_dict_type_code
        self.data_dict_ids = data_dict_ids
        super().__init__(*args)

    def get_worker(self) -> QueryDataDictBindDataWorker:
        return QueryDataDictBindDataWorker(self.data_dict_type_code, self.data_dict_ids)

# ----------------------- 查询数据字典是否关联数据 end ----------------------- #
