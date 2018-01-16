#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017~2999 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import functools
import threading

def lock(func):
    ''' use `Lock` to keep func access thread-safety. '''
    sync = threading.Lock()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with sync:
            return func(*args, **kwargs)

    return wrapper

def rlock(func):
    ''' use `RLock` to keep func access thread-safety. '''
    sync = threading.RLock()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with sync:
            return func(*args, **kwargs)

    return wrapper
