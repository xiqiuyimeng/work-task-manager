# -*- coding: utf-8 -*-
from src.service.system_storage.task_sqlite import TaskSqlite

_author_ = 'luwt'
_date_ = '2023/7/27 17:11'


task_names = list()


def init_task_names():
    global task_names
    task_names = TaskSqlite().get_task_names()


def get_task_names():
    return task_names


def update_task_name(origin_task_name, new_task_name):
    task_names.remove(origin_task_name)
    task_names.append(new_task_name)


def add_task_names(task_name):
    task_names.append(task_name)


def del_task_names(deleted_task_names):
    for task_name in deleted_task_names:
        task_names.remove(task_name)
