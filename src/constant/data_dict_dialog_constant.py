# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/7/15 10:52'


DATA_DICT_TYPE_LIST_TITLE = '数据字典类型列表'
DATA_DICT_DETAIL_TITLE = '数据字典 [{}] 明细'

# 数据字典类型
PRIORITY = '优先级'
TASK_TYPE = '任务类型'
DEMAND_PERSON = '任务需求方'
TASK_STATUS = '任务状态'
PUBLISH_STATUS = '发版状态'
PUBLISH_TYPE = '发版信息类型'

# 默认类型值列表
PRIORITY_VALUES = (
    {
        'dict_name': '最高',
        'font_color': 'rgba(255,240,23,255)',
        'background_color': 'rgba(255,68,5,255)'
    },
    {
        'dict_name': '高',
        'font_color': 'rgba(255,255,127,200)',
        'background_color': 'rgba(255,93,44,196)'
    },
    {
        'dict_name': '中',
        'font_color': 'rgba(255,19,35,255)',
        'background_color': 'rgba(23,124,255,129)'
    },
    {
        'dict_name': '低',
        'font_color': 'rgba(0,0,0,255)',
        'background_color': 'rgba(203,255,245,255)'
    },
)
TASK_TYPE_VALUES = (
    {
        'dict_name': '产品需求',
        'background_color': 'rgba(255,175,14,128)'
    },
    {
        'dict_name': '线上bug',
        'background_color': 'rgba(255,227,221,255)'
    },
    {
        'dict_name': '代码优化',
        'background_color': 'rgba(216,255,172,255)'
    },
    {
        'dict_name': '业务问题',
        'background_color': 'rgba(255,41,173,96)'
    },
)
DEMAND_PERSON_VALUES = ('业务', '产品')
TASK_STATUS_VALUES = ('提出任务', '设计分析', '开发中', '开发完成', '发布测试', '发布生产', '完成')
PUBLISH_STATUS_VALUES = ('无需发版', '未发版', '已发版')
PUBLISH_TYPE_VALUES = ('数据库', '代码配置', '前端代码', '后端代码', '其他')

# 数据字典类型列表操作提示语
DATA_DICT_TYPE_OPERATION_TIP = '温馨提示：双击数据字典类型即可进入详情页'
# 数据字典详情温馨提示语
DATA_DICT_DETAIL_TIP = '温馨提示：在页面操作后，请点击 [保存] 按钮保存修改内容后退出'

# 数据字典详情 按钮
SYNC_DEFAULT_DATA_DICT_BTN_TEXT = '同步默认数据字典'
SORT_DATA_DICT_BUTTON_TEXT = '排序'
ADD_DATA_DICT_BTN_TEXT = '添加'
DEL_DATA_DICT_BTN_TEXT = '删除'

# 字典名称重复提示语
DUPLICATE_DATA_DICT_NAME_PROMPT = '字典名称已存在，请重新填写'

# 字典名称存在空值
BLANK_DATA_DICT_NAME_PROMPT = '字典名称不允许为空，请先填写字典名称'

# 字典为空，且需要转移数据时，不允许保存
NO_DATA_DICT_PROMPT = '已删除的字典项绑定了数据，新的字典项不能为空，否则无法重新绑定数据，\n请先添加字典项再保存数据'

DATA_DICT_DETAIL_BOX_TITLE = '保存数据字典'
QUERY_DATA_DICT_BIND_DATA_TITLE = '查询数据字典绑定数据情况'

MAINTAIN_DATA_DICT_BIND_TITLE = '数据字典绑定数据维护'
DATA_DICT_HEADER_TEXT = '新的数据字典值列表'
ORIGIN_DATA_DICT_HEADER_TEXT = '已删除的数据字典列表'
DATA_DICT_BIND_ARROW_TEXT = '-------------------->'
DATA_DICT_COMBOBOX_PLACEHOLDER_TEXT = '请选择数据字典值'

CHECK_COMBOBOX_PROMPT = '已删除字典项数据存在未绑定新字典项，请检查'
CHECK_COMBOBOX_TITLE = '检查字典项'

DATA_DICT_SORT_TITLE = '数据字典排序'
DATA_DICT_SORT_BOX_TITLE = '数据字典排序'
