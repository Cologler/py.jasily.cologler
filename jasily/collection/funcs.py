# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from functools import partial
from typing import Callable, List, Any

def call_each(funcs: List[Callable[[], Any]]):
    '''
    call each func from func list.

    return the last func value or None if func list is empty.
    '''
    ret = None
    for func in funcs:
        ret = func()
    return ret

def call_each_reversed(funcs: List[Callable[[], Any]]):
    '''
    call each func from reversed func list.

    return the last func value or None if func list is empty.
    '''
    ret = None
    for func in reversed(funcs):
        ret = func()
    return ret

class CallableList(list):
    '''
    a simple callable list.
    '''

    def __call__(self):
        return call_each(self)

    def append_func(self, func, *args, **kwargs):
        '''
        append func with given arguments and keywords.
        '''
        wraped_func = partial(func, *args, **kwargs)
        self.append(wraped_func)

    def insert_func(self, index, func, *args, **kwargs):
        '''
        insert func with given arguments and keywords.
        '''
        wraped_func = partial(func, *args, **kwargs)
        self.insert(index, wraped_func)
