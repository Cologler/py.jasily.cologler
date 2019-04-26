# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import functools

from ..data.box import Box

def once(func):
    '''
    only call the func once, ignore if call again.

    return value always be `None`.
    '''
    is_call = False

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal is_call
        if is_call:
            return
        is_call = True
        func(*args, **kwargs)

    return wrapper

def assert_once(func):
    '''
    only call the func once, assert false if call again.

    return value always be `None`.
    '''
    is_call = False

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal is_call
        if is_call:
            assert False, 'func cannot call again'
            return
        is_call = True
        func(*args, **kwargs)

    return wrapper
