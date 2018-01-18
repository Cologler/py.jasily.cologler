#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import contextlib
import functools

def with_it(obj):
    '''
    wrap `with obj` out of func.
    '''

    def _wrap(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with obj:
                return func(*args, **kwargs)

        return wrapper

    return _wrap

def with_objattr(name):
    '''
    wrap `with getattr(self, name)` out of func.

    usage:

    ``` py
    class A:
        def __init__(self):
            self._lock = RLock()

        @with_objattr('_lock') # so easy to make a sync instance method !
        def func():
            pass
    ```
    '''

    def _wrap(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            with getattr(self, name):
                return func(self, *args, **kwargs)

        return wrapper

    return _wrap

def with_objattrs(*names):
    '''
    like `with_objattr` but enter context one by one.
    '''

    def _wrap(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            with contextlib.ExitStack() as stack:
                for name in names:
                    stack.enter_context(getattr(self, name))
                return func(self, *args, **kwargs)

        return wrapper

    return _wrap
