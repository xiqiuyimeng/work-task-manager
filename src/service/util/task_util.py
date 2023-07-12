# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/7/11 17:22'


def collect_data_dict_ids(data_dict_ids, task):
    data_dict_ids.append(task.task_type_id)
    data_dict_ids.append(task.demand_person_id)
    data_dict_ids.append(task.priority_id)
    data_dict_ids.append(task.status_id)
    data_dict_ids.append(task.publish_status_id)


def set_data_dict_obj(data_id_dict, task):
    task.task_type = data_id_dict.get(task.task_type_id)
    task.demand_person = data_id_dict.get(task.demand_person_id)
    task.priority = data_id_dict.get(task.priority_id)
    task.status = data_id_dict.get(task.status_id)
    task.publish_status = data_id_dict.get(task.publish_status_id)
