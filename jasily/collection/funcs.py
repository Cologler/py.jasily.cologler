# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from functools import partial

def call_each(funcs: list, *args, **kwargs):
    '''
    call each func from func list.

    return the last func value or None if func list is empty.
    '''
    ret = None
    for func in funcs:
        ret = func(*args, **kwargs)
    return ret

def call_each_reversed(funcs: list, *args, **kwargs):
    '''
    call each func from reversed func list.

    return the last func value or None if func list is empty.
    '''
    ret = None
    for func in reversed(funcs):
        ret = func(*args, **kwargs)
    return ret


class CallableList(list):
    '''
    a simple callable list.
    '''

    def __call__(self, *args, **kwargs):
        return call_each(self, *args, **kwargs)

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
