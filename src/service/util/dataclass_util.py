# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/7/10 15:30'


def init(cls):
    """给数据类增加init方法"""
    def __init__(cls_obj, **kwargs):
        for k, v in kwargs.items():
            setattr(cls_obj, k, v)
    cls.__init__ = __init__
    return cls
