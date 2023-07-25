# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.system_storage.project_sqlite import ProjectSqlite
from src.service.system_storage.task_sqlite import TaskSqlite
from src.service.util.project_cache_util import update_project_dict, remove_project
from src.view.box.message_box import pop_ok

_author_ = 'luwt'
_date_ = '2023/7/19 6:59'


# ----------------------- 添加项目 start ----------------------- #

class AddProjectWorker(ThreadWorkerABC):
    success_signal = pyqtSignal()

    def __init__(self, project):
        super().__init__()
        self.project = project

    def do_run(self):
        log.info(f'开始添加项目 {self.project.project_name}')
        # 持久化到数据库
        ProjectSqlite().add_project(self.project)
        # 更新缓存数据
        update_project_dict(self.project)
        self.success_signal.emit()
        log.info(f'添加项目成功 {self.project.project_name}')

    def get_err_msg(self) -> str:
        return f'添加项目失败 {self.project.project_name}'


class AddProjectExecutor(LoadingMaskThreadExecutor):

    def __init__(self, project, *args):
        self.project = project
        super().__init__(*args)

    def get_worker(self) -> AddProjectWorker:
        return AddProjectWorker(self.project)

    def success_post_process(self, *args):
        pop_ok(f'添加项目成功 {self.project.project_name}', self.error_box_title, self.window)
        super().success_post_process()


# ----------------------- 添加项目 end ----------------------- #


# ----------------------- 编辑项目 start ----------------------- #

class EditProjectWorker(ThreadWorkerABC):
    success_signal = pyqtSignal()

    def __init__(self, project):
        super().__init__()
        self.project = project

    def do_run(self):
        log.info(f'开始编辑项目 {self.project.project_name}')
        # 持久化到数据库
        ProjectSqlite().update_by_id(self.project)
        # 更新缓存数据
        update_project_dict(self.project)
        self.success_signal.emit()
        log.info(f'编辑项目成功 {self.project.project_name}')

    def get_err_msg(self) -> str:
        return f'编辑项目失败 {self.project.project_name}'


class EditProjectExecutor(LoadingMaskThreadExecutor):

    def __init__(self, project, *args):
        self.project = project
        super().__init__(*args)

    def get_worker(self) -> EditProjectWorker:
        return EditProjectWorker(self.project)

    def success_post_process(self, *args):
        pop_ok(f'编辑项目成功 {self.project.project_name}', self.error_box_title, self.window)
        super().success_post_process()


# ----------------------- 编辑项目 end ----------------------- #


# ----------------------- 删除项目 start ----------------------- #

class DelProjectWorker(ThreadWorkerABC):
    success_signal = pyqtSignal()

    def __init__(self, project_ids, project_names):
        super().__init__()
        self.project_ids = project_ids
        self.project_names = project_names

    def do_run(self):
        log.info(f'开始删除项目 {self.project_names}')
        # 检查是否存在子任务，如果存在，不允许删除
        task_used_project_ids = TaskSqlite().get_used_project_ids(self.project_ids)
        if task_used_project_ids:
            used_project_names = [self.project_names[self.project_ids.index(project_id)]
                                  for project_id in task_used_project_ids]
            used_project_name_str = '\n'.join(used_project_names)
            raise Exception(f'以下项目已存在子任务，请先删除项目关联的任务，或解除任务与项目的关系，'
                            f'再删除项目\n{used_project_name_str}')
        # 删除项目
        ProjectSqlite().delete_by_ids(self.project_ids)
        # 更新缓存数据
        remove_project(self.project_ids)
        self.success_signal.emit()
        log.info(f'删除项目成功 {self.project_names}')

    def get_err_msg(self) -> str:
        return f'删除项目失败 {self.project_names}'


class DelProjectExecutor(LoadingMaskThreadExecutor):

    def __init__(self, project_id, project_name, row_index, *args):
        self.project_id = project_id
        self.project_name = project_name
        self.row_index = row_index
        super().__init__(*args)

    def get_worker(self) -> DelProjectWorker:
        return DelProjectWorker((self.project_id,), (self.project_name,))

    def success_post_process(self, *args):
        self.success_callback(self.row_index)


class BatchDelProjectExecutor(LoadingMaskThreadExecutor):

    def __init__(self, project_ids, project_names, delete_index_list, *args):
        self.project_ids = project_ids
        self.project_names = project_names
        self.delete_index_list = delete_index_list
        super().__init__(*args)

    def get_worker(self) -> DelProjectWorker:
        return DelProjectWorker(self.project_ids, self.project_names)

    def success_post_process(self, *args):
        self.success_callback(self.delete_index_list)

# ----------------------- 删除项目 end ----------------------- #
