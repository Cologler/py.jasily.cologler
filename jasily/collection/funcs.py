# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from functools import partial

class CallableList(list):
    '''
    a simple callable list.
    '''

    def __call__(self):
        ret = None
        for func in self:
            ret = func()
        return ret

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
