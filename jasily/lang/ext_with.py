#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import functools

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
