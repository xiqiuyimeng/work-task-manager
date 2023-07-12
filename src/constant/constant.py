# -*- coding: utf-8 -*-
import os

_author_ = 'luwt'
_date_ = '2023/7/10 12:26'


# windows家目录变量：USERPROFILE，unix：HOME
SYS_DB_PATH = os.path.join(os.environ['USERPROFILE'], '.work_task_manager_db')
