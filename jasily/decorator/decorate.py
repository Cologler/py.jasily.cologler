# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import functools

def decorate(target):
    '''
    a replacment for `functools.wraps()`.
    '''

    def wrap(func):

        if isinstance(target, type):
            def __init__(self, *args, **kwargs):
                func(*args, **kwargs)

            wrapper = type(target)(target.__name__, (target, ), {
                '__init__': __init__
            })
            functools.update_wrapper(wrapper, target, updated=())

        else:
            wrapper = func
            functools.update_wrapper(wrapper, target)

        return wrapper

    return wrap
